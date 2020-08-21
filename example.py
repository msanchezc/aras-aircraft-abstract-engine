from aras_aircraft_abstract_engine.template import ArasAircraftAbstractEngine
aircraft_engine = ArasAircraftAbstractEngine()
aircraft_engine.start_takeoff = lambda x: print("hello world 1")
aircraft_engine.start_go_up = lambda x: print("hello world 2")
aircraft_engine.run_server(port="50052")
