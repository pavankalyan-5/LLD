
class ParkingStrategy:
    def park(self, floors: list['ParkingFloor'], vehicle_type: int) -> str:
        pass


class NearestParkingSlotStrategy(ParkingStrategy):
    def park(self, floors: list, vehicle_type: int) -> str:
        for floor in floors:
            spot_id = floor.park(vehicle_type)
            if spot_id:
                return spot_id
        return ""

class MostFreeFloorParkingSlotStrategy(ParkingStrategy):
    def park(self, floors: list, vehicle_type: int) -> str:
        max_free_parking_spots = 0
        floor_index = -1
        for i, floor in enumerate(floors):
            free_parking_spots = floor.free_spots_available.get(vehicle_type, 0)
            if max_free_parking_spots < free_parking_spots:
                max_free_parking_spots = free_parking_spots
                floor_index = i
        
        if floor_index != -1:
            return floors[floor_index].park(vehicle_type)
        return ""


class ParkingManager:
    def __init__(self):
        self.algorithms = [NearestParkingSlotStrategy(), MostFreeFloorParkingSlotStrategy()]
    

    def park(self, floors: list, vehicle_type: int, parking_strategy: int):
        self.algorithms[parking_strategy].park(floors, vehicle_type)


class SearchManager:
    def __init__(self):
        self.cache = {}

    def search(self, query: str) -> str:
        return self.cache.get(query, "")

    def index(self, spot_id: str, vehicle_number: str, ticket_id: str):
        self.cache[vehicle_number] = spot_id
        self.cache[ticket_id] = spot_id


class Solution:

    def init(self, helper, parking: list[list[list[int]]]):
        """
        Initialize the parking lot with the given helper and parking structure.
        """
        self.helper = helper
        self.vehicle_types = [2, 4]
        self.floors = [ParkingFloor(i, parking[i], self.vehicle_types, helper) for i in parking]
        self.parking_manager = ParkingManager()
        self.search_manager = SearchManager()
        #helper.println(" floors initialized ")
        

    def park(self, vehicle_type: int, vehicle_number: str, ticket_id: str, parking_strategy: int) -> str:
        """
        Park a vehicle in the parking lot.
        
        Args:
            vehicle_type (int): Type of the vehicle.
            vehicle_number (str): Number of the vehicle.
            ticket_id (str): Ticket ID of the vehicle.
            parking_strategy (int): Strategy for parking the vehicle.

        Returns:
            str: The spot ID where the vehicle is parked.
        """
        spot_id = self.parking_manager.park(self.floors, vehicle_type, parking_strategy)
        if spot_id:
            self.search_manager.index(spot_id, vehicle_number, ticket_id)
        return spot_id

    def remove_vehicle(self, spot_id: str) -> bool:
        """
        Remove a vehicle from the parking lot.
        
        Args:
            spot_id (str): The spot ID where the vehicle is parked.

        Returns:
            bool: True if the vehicle was removed, False otherwise.
        """
        floor_index, row, col = map(int, spot_id.split('-'))
        return self.floors[floor_index].remove_vehicle(row, col)

    def get_free_spots_count(self, floor: int, vehicle_type: int) -> int:
        """
        Get the count of free spots for a given vehicle type on a specific floor.
        
        Args:
            floor (int): The floor number.
            vehicle_type (int): The vehicle type.

        Returns:
            int: The number of free spots available.
        """
        return self.floors[floor].free_spots_available.get(vehicle_type, 0)

    def search_vehicle(self, query: str) -> str:
        """
        Search for a vehicle by its number or ticket ID.
        
        Args:
            query (str): The vehicle number or ticket ID.

        Returns:
            str: The spot ID where the vehicle is parked.
        """
        return self.search_manager.search(query)
    

class ParkingFloor:
    def __init__(self, floor_number: int, parking_floor:list[list[int]], vehicle_types:list[int], helper):
        
        # no cars placed
        self.parking_spots = [[None] * len(parking_floor[0]) for _ in parking_floor]
        self.free_spots_available = {vt:0 for vt in vehicle_types}

        for lane in parking_floor:
            for spot in lane:
                vehicle_type = parking_floor[lane][spot]
                if vehicle_type != 0:
                    self.parking_spots = [ParkingSlot(vehicle_type, f"{floor_number}-{lane}-{spot}")]
                    self.free_spots_available[vehicle_type] += 1
    
    def park(self, vehicle_type: str):
        if self.free_spots_available.get(vehicle_type, 0) == 0:
            return ""
        for lane in self.parking_spots:
            for spot in lane:
                if spot is None and not spot.is_parked() and spot.get_vehicle_type() == vehicle_type:
                    self.free_spots_available[vehicle_type] -= 1
                    spot.park_vehicle()
                    spot_id = spot.get_spot_id()
                    return spot_id
        return ""
    
    def remove_vehicle(self, row, col):
        if row < 0 or row > len(self.parking_spots) - 1 or col < 0 or col > len(self.parking_spots[row]) - 1 or not self.parking_spots[row][col].is_parked():
            False 
        
        vehicle_type = self.parking_spots[row][col].get_vehicle_type()
        self.parking_spots[row][col].remove_vehicle()
        self.free_spots_available[vehicle_type] += 1

        return self.parking_spots[row][col].get_spot_id()





class ParkingSlot:
    def __init__(self, vehicle_type, spot_id) :
        self.spot_id = spot_id
        self.vehicle_type = vehicle_type
        self.is_slot_parked = False

    def remove_vehicle(self):
        self.is_slot_parked = False
    
    def park_vehicle(self):
        self.is_slot_parked = True
    
    def is_parked(self):
        return self.is_slot_parked
    
    def get_spot_id(self):
        return self.spot_id
    
    def get_vehicle_type(self):
        return self.vehicle_type
        