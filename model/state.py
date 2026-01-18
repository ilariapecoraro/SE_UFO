from dataclasses import dataclass,field

@dataclass
class State:
    id: int
    name: str
    capital: str
    lat: float
    lng: float
    area: float
    population: int
    neighbors: list = field(default_factory=list)



    def __repr__(self):
        return f"{self.id}"

    # Serve per poter usare l'oggetto come nodo del grafo
    def __hash__(self):
        return hash(self.id)

