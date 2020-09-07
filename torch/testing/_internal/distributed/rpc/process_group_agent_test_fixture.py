import torch.distributed.rpc as rpc
from torch.testing._internal.distributed.rpc.rpc_agent_test_fixture import (
    RpcAgentTestFixture,
)


class ProcessGroupRpcAgentTestFixture(RpcAgentTestFixture):
    @property
    def rpc_backend(self):
        return rpc.backend_registry.BackendType[
            "PROCESS_GROUP"
        ]

    @property
    def rpc_backend_options(self):
        return rpc.backend_registry.construct_rpc_backend_options(
            self.rpc_backend,
            init_method=self.init_method,
            # Some tests need additional threads (ex: test_trainer_ps)
            num_send_recv_threads=8,
        )

    def get_shutdown_error_regex(self):
        error_regexes = [
            "Encountered exception in ProcessGroupAgent::enqueueSend",
            "Encountered exception in ProcessGroupAgent::listenLoop()",
            "Exception in thread pool task",
            "Connection reset by peer",
            "Connection closed by peer",
            "RPC ran for more than \d+(\d+)* milliseconds and timed out"  # noqa: W605
        ]
        return "|".join(["({})".format(error_str) for error_str in error_regexes])

    def get_timeout_error_regex(self):
        return "RPC ran for more than"
