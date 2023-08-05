""" A minimal application base mixin for all ZMQ based IPython frontends.

This is not a complete console app, as subprocess will not be able to receive
input, there is no real readline support, among other limitations. This is a
refactoring of what used to be the IPython/qt/console/qtconsoleapp.py
"""
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import atexit
import os
import signal
import sys
import uuid
import warnings


from traitlets.config.application import boolean_flag
from ipython_genutils.path import filefind
from traitlets import (
    Dict, List, Unicode, CUnicode, CBool, Any
)

from jupyter_core.application import base_flags, base_aliases

from .blocking import BlockingKernelClient
from .restarter import KernelRestarter
from . import KernelManager, tunnel_to_kernel, find_connection_file, connect
from .kernelspec import NoSuchKernel
from .session import Session

ConnectionFileMixin = connect.ConnectionFileMixin

from .localinterfaces import localhost

#-----------------------------------------------------------------------------
# Aliases and Flags
#-----------------------------------------------------------------------------

flags = {}
flags.update(base_flags)
# the flags that are specific to the frontend
# these must be scrubbed before being passed to the kernel,
# or it will raise an error on unrecognized flags
app_flags = {
    'existing' : ({'JupyterConsoleApp' : {'existing' : 'kernel*.json'}},
            "Connect to an existing kernel. If no argument specified, guess most recent"),
}
app_flags.update(boolean_flag(
    'confirm-exit', 'JupyterConsoleApp.confirm_exit',
    """Set to display confirmation dialog on exit. You can always use 'exit' or
       'quit', to force a direct exit without any confirmation. This can also
       be set in the config file by setting
       `c.JupyterConsoleApp.confirm_exit`.
    """,
    """Don't prompt the user when exiting. This will terminate the kernel
       if it is owned by the frontend, and leave it alive if it is external.
       This can also be set in the config file by setting
       `c.JupyterConsoleApp.confirm_exit`.
    """
))
flags.update(app_flags)

aliases = {}
aliases.update(base_aliases)

# also scrub aliases from the frontend
app_aliases = dict(
    ip = 'JupyterConsoleApp.ip',
    transport = 'JupyterConsoleApp.transport',
    hb = 'JupyterConsoleApp.hb_port',
    shell = 'JupyterConsoleApp.shell_port',
    iopub = 'JupyterConsoleApp.iopub_port',
    stdin = 'JupyterConsoleApp.stdin_port',
    existing = 'JupyterConsoleApp.existing',
    f = 'JupyterConsoleApp.connection_file',

    kernel = 'JupyterConsoleApp.kernel_name',

    ssh = 'JupyterConsoleApp.sshserver',
)
aliases.update(app_aliases)

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

classes = [KernelManager, KernelRestarter, Session]

class JupyterConsoleApp(ConnectionFileMixin):
    name = 'jupyter-console-mixin'

    description = """
        The Jupyter Console Mixin.
        
        This class contains the common portions of console client (QtConsole,
        ZMQ-based terminal console, etc).  It is not a full console, in that
        launched terminal subprocesses will not be able to accept input.
        
        The Console using this mixing supports various extra features beyond
        the single-process Terminal IPython shell, such as connecting to
        existing kernel, via:
        
            jupyter console <appname> --existing
        
        as well as tunnel via SSH
        
    """

    classes = classes
    flags = Dict(flags)
    aliases = Dict(aliases)
    kernel_manager_class = KernelManager
    kernel_client_class = BlockingKernelClient

    kernel_argv = List(Unicode())

    # connection info:
    
    sshserver = Unicode('', config=True,
        help="""The SSH server to use to connect to the kernel.""")
    sshkey = Unicode('', config=True,
        help="""Path to the ssh key to use for logging in to the ssh server.""")
    
    def _connection_file_default(self):
        return 'kernel-%i.json' % os.getpid()

    existing = CUnicode('', config=True,
        help="""Connect to an already running kernel""")

    kernel_name = Unicode('python', config=True,
        help="""The name of the default kernel to start.""")

    confirm_exit = CBool(True, config=True,
        help="""
        Set to display confirmation dialog on exit. You can always use 'exit' or 'quit',
        to force a direct exit without any confirmation.""",
    )
    
    def build_kernel_argv(self, argv=None):
        """build argv to be passed to kernel subprocess
        
        Override in subclasses if any args should be passed to the kernel
        """
        self.kernel_argv = self.extra_args
    
    def init_connection_file(self):
        """find the connection file, and load the info if found.
        
        The current working directory and the current profile's security
        directory will be searched for the file if it is not given by
        absolute path.
        
        When attempting to connect to an existing kernel and the `--existing`
        argument does not match an existing file, it will be interpreted as a
        fileglob, and the matching file in the current profile's security dir
        with the latest access time will be used.
        
        After this method is called, self.connection_file contains the *full path*
        to the connection file, never just its name.
        """
        if self.existing:
            try:
                cf = find_connection_file(self.existing, ['.', self.runtime_dir])
            except Exception:
                self.log.critical("Could not find existing kernel connection file %s", self.existing)
                self.exit(1)
            self.log.debug("Connecting to existing kernel: %s" % cf)
            self.connection_file = cf
        else:
            # not existing, check if we are going to write the file
            # and ensure that self.connection_file is a full path, not just the shortname
            try:
                cf = find_connection_file(self.connection_file, [self.runtime_dir])
            except Exception:
                # file might not exist
                if self.connection_file == os.path.basename(self.connection_file):
                    # just shortname, put it in security dir
                    cf = os.path.join(self.runtime_dir, self.connection_file)
                else:
                    cf = self.connection_file
                self.connection_file = cf
        try:
            self.connection_file = filefind(self.connection_file, ['.', self.runtime_dir])
        except IOError:
            self.log.debug("Connection File not found: %s", self.connection_file)
            return
        
        # should load_connection_file only be used for existing?
        # as it is now, this allows reusing ports if an existing
        # file is requested
        try:
            self.load_connection_file()
        except Exception:
            self.log.error("Failed to load connection file: %r", self.connection_file, exc_info=True)
            self.exit(1)
    
    def init_ssh(self):
        """set up ssh tunnels, if needed."""
        if not self.existing or (not self.sshserver and not self.sshkey):
            return
        self.load_connection_file()
        
        transport = self.transport
        ip = self.ip
        
        if transport != 'tcp':
            self.log.error("Can only use ssh tunnels with TCP sockets, not %s", transport)
            sys.exit(-1)
        
        if self.sshkey and not self.sshserver:
            # specifying just the key implies that we are connecting directly
            self.sshserver = ip
            ip = localhost()
        
        # build connection dict for tunnels:
        info = dict(ip=ip,
                    shell_port=self.shell_port,
                    iopub_port=self.iopub_port,
                    stdin_port=self.stdin_port,
                    hb_port=self.hb_port
        )
        
        self.log.info("Forwarding connections to %s via %s"%(ip, self.sshserver))
        
        # tunnels return a new set of ports, which will be on localhost:
        self.ip = localhost()
        try:
            newports = tunnel_to_kernel(info, self.sshserver, self.sshkey)
        except:
            # even catch KeyboardInterrupt
            self.log.error("Could not setup tunnels", exc_info=True)
            self.exit(1)
        
        self.shell_port, self.iopub_port, self.stdin_port, self.hb_port = newports
        
        cf = self.connection_file
        root, ext = os.path.splitext(cf)
        self.connection_file = root + '-ssh' + ext
        self.write_connection_file() # write the new connection file
        self.log.info("To connect another client via this tunnel, use:")
        self.log.info("--existing %s" % os.path.basename(self.connection_file))
    
    def _new_connection_file(self):
        cf = ''
        while not cf:
            # we don't need a 128b id to distinguish kernels, use more readable
            # 48b node segment (12 hex chars).  Users running more than 32k simultaneous
            # kernels can subclass.
            ident = str(uuid.uuid4()).split('-')[-1]
            cf = os.path.join(self.runtime_dir, 'kernel-%s.json' % ident)
            # only keep if it's actually new.  Protect against unlikely collision
            # in 48b random search space
            cf = cf if not os.path.exists(cf) else ''
        return cf

    def init_kernel_manager(self):
        # Don't let Qt or ZMQ swallow KeyboardInterupts.
        if self.existing:
            self.kernel_manager = None
            return
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Create a KernelManager and start a kernel.
        try:
            self.kernel_manager = self.kernel_manager_class(
                                    ip=self.ip,
                                    session=self.session,
                                    transport=self.transport,
                                    shell_port=self.shell_port,
                                    iopub_port=self.iopub_port,
                                    stdin_port=self.stdin_port,
                                    hb_port=self.hb_port,
                                    connection_file=self.connection_file,
                                    kernel_name=self.kernel_name,
                                    parent=self,
                                    data_dir=self.data_dir,
            )
        except NoSuchKernel:
            self.log.critical("Could not find kernel %s", self.kernel_name)
            self.exit(1)

        self.kernel_manager.client_factory = self.kernel_client_class
        # FIXME: remove special treatment of IPython kernels
        kwargs = {}
        if self.kernel_manager.ipykernel:
            kwargs['extra_arguments'] = self.kernel_argv
        self.kernel_manager.start_kernel(**kwargs)
        atexit.register(self.kernel_manager.cleanup_ipc_files)

        if self.sshserver:
            # ssh, write new connection file
            self.kernel_manager.write_connection_file()

        # in case KM defaults / ssh writing changes things:
        km = self.kernel_manager
        self.shell_port=km.shell_port
        self.iopub_port=km.iopub_port
        self.stdin_port=km.stdin_port
        self.hb_port=km.hb_port
        self.connection_file = km.connection_file

        atexit.register(self.kernel_manager.cleanup_connection_file)

    def init_kernel_client(self):
        if self.kernel_manager is not None:
            self.kernel_client = self.kernel_manager.client()
        else:
            self.kernel_client = self.kernel_client_class(
                                session=self.session,
                                ip=self.ip,
                                transport=self.transport,
                                shell_port=self.shell_port,
                                iopub_port=self.iopub_port,
                                stdin_port=self.stdin_port,
                                hb_port=self.hb_port,
                                connection_file=self.connection_file,
                                parent=self,
            )

        self.kernel_client.start_channels()



    def initialize(self, argv=None):
        """
        Classes which mix this class in should call:
               JupyterConsoleApp.initialize(self,argv)
        """
        if self._dispatching:
            return
        self.init_connection_file()
        self.init_ssh()
        self.init_kernel_manager()
        self.init_kernel_client()

class IPythonConsoleApp(JupyterConsoleApp):
    def __init__(self, *args, **kwargs):
        warnings.warn("IPythonConsoleApp is deprecated. Use JupyterConsoleApp")
        super(IPythonConsoleApp, self).__init__(*args, **kwargs)
