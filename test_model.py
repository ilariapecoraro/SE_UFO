from model.model import Model

model = Model()
g = model.build_graph(1999, "triangle")
cammino = model.ricerca_cammino()
print(cammino)
print(model.best_path)