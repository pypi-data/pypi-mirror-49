#!/usr/bin/python3

import json


# network

class UnknownAccount(Exception):
    pass


class UndeployedLibrary(Exception):
    pass


class _RPCBaseException(Exception):

    def __init__(self, msg, cmd, proc, uri):
        code = proc.poll()
        out = proc.stdout.read().decode().strip() or "  (Empty)"
        err = proc.stderr.read().decode().strip() or "  (Empty)"
        super().__init__(
            f"{msg}\n\nCommand: {cmd}\nURI: {uri}\nExit Code: {code}"
            f"\n\nStdout:\n{out}\n\nStderr:\n{err}"
        )


class RPCProcessError(_RPCBaseException):

    def __init__(self, cmd, proc, uri):
        super().__init__("Unable to launch local RPC client.", cmd, proc, uri)


class RPCConnectionError(_RPCBaseException):

    def __init__(self, cmd, proc, uri):
        super().__init__("Able to launch RPC client, but unable to connect.", cmd, proc, uri)


class RPCRequestError(Exception):
    pass


class VirtualMachineError(Exception):

    '''Raised when a call to a contract causes an EVM exception.

    Attributes:
        revert_msg: The returned error string, if any.
        source: The contract source code where the revert occured, if available.'''

    revert_msg = ""
    source = ""

    def __init__(self, exc):
        if type(exc) is not dict:
            try:
                exc = eval(str(exc))
            except SyntaxError:
                exc = {'message': str(exc)}
        if len(exc['message'].split('revert ', maxsplit=1)) > 1:
            self.revert_msg = exc['message'].split('revert ')[-1]
        if 'source' in exc:
            self.source = exc['source']
            super().__init__(exc['message']+"\n"+exc['source'])
        else:
            super().__init__(exc['message'])


# project/

class ContractExists(Exception):
    pass


class ProjectAlreadyLoaded(Exception):
    pass


class ProjectNotFound(Exception):
    pass


class CompilerError(Exception):

    def __init__(self, e):
        err = [i['formattedMessage'] for i in json.loads(e.stdout_data)['errors']]
        super().__init__("Compiler returned the following errors:\n\n"+"\n".join(err))


# test/

class ExpectedFailing(Exception):
    pass


# types/

class InvalidABI(Exception):
    pass
