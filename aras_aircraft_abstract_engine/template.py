import asyncio
import logging
import threading

from grpc.experimental import aio
from aras_control_service_protocol.generated import protocol_pb2
from aras_control_service_protocol.generated import protocol_pb2_grpc


class ArasAircraftAbstractEngine(protocol_pb2_grpc.ControlServiceActions):
    @staticmethod
    def _generic_error(method_name):
        def f(useless):
            raise Exception(
                "No definition found to %s" % method_name)
        return f

    def __init__(self):
        self.start_takeoff = ArasAircraftAbstractEngine._generic_error(
            "start_takeoff")
        self.start_go_up = ArasAircraftAbstractEngine._generic_error(
            "start_go_up")

    # ------------------ Start take off actions --------------------------

    async def StartTakeoff(self, request, context):
        drone = request
        t = threading.Thread(target=self.start_takeoff, args=[drone])
        t.start()
        return protocol_pb2.ACK()

    # ------------------ End take off actions ---------------------------

    # ------------------ Start go up actions ----------------------------

    async def StartGoUp(self, request, context):
        go_up_message = request
        t = threading.Thread(target=self.start_go_up, args=[go_up_message])
        t.start()
        return protocol_pb2.ACK()

    # ------------------ End go up actions ------------------------------

    async def _start_async_server(self, port):
        server = aio.server()
        server.add_insecure_port("[::]:%s" % port)
        protocol_pb2_grpc.add_ControlServiceActionsServicer_to_server(
            self, server
        )
        await server.start()
        await server.wait_for_termination()

    def run_server(self, port):
        logging.basicConfig()
        loop = asyncio.get_event_loop()
        loop.create_task(self._start_async_server(port))
        loop.run_forever()
