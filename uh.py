from pyomo.environ import *
from pyomo.opt import SolverFactory
from io import StringIO
import csv

model = ConcreteModel()

## La diferentes secciones que se pueden tomar de un curso
model.c = RangeSet(1, 5)

## Las horas que puede pcupar cada sección
model.h = RangeSet(1, 10)

## Materias que se pueden meter
model.s = RangeSet(1, 3)



def convert_to_dict(csv_string: str):
    csv_io = StringIO(csv_string)
    tuple_dict = {}
    csv_reader = csv.reader(csv_io)
    next(csv_reader)
    for i, row in enumerate(csv_reader):
        if i == 0:
            continue
        for j, item in enumerate(row):
            if j == 0:
                continue
            print(i, j, item)
            tuple_dict[(int(i), int(j))] = int(item)
    return tuple_dict


## Una tabla que indica las horas específicas que ocupa casa seccion, si la sección usa la hora se marca como 1, sino es 0
seccion_usa_hora = convert_to_dict("""
@,c1,c2,c3,c4,c5
h1,0,0,1,0,0
h2,0,1,0,0,0
h3,0,0,1,0,0
h4,1,0,0,0,0
h5,0,0,0,1,0
h6,1,0,0,0,0
h7,0,1,0,0,0
h8,0,0,0,0,1
h9,0,0,0,0,1
h10,0,0,0,1,0
""")


## Tabla que indica si una sección pertenece a una materia, 
## si sí entonces se marca con 1, si no es de esa materia entonces es 0
seccion_pertenece_clase = convert_to_dict("""
@@,c1,c2,c3,c4,c5
s1,0,0,0,1,1
s2,1,1,0,0,0
s3,0,0,1,0,0
""")

model.u = seccion_usa_hora
model.p = seccion_pertenece_clase

## indíca en numero de créditos de cada sección 
model.cr = Param(model.c, initialize={1: 3, 2: 3, 3: 4, 4: 2, 5: 2})

## Indica el rating del profesor de cada sección
model.rat = Param(model.c, initialize={1: 2.5, 2: 4, 3: 3.5, 4: 5, 5: 2})

## Es una variable que indica si se escogió alguna sección de una clase
model.el = Var(model.c, domain=Binary)

## Indica el límite de créditos que puede ver el estudiante en el semestre
LIMITE_CREDITOS = 10

## ïndica el mínimo de créditos que quiere meter el estudiante en el semestre
MINIMO_CREDITOS = 8

## Una variable que indica el promedio del rating de todas las clases escogidas
model.r = Var()

def objective_rule(model: ConcreteModel):
    return sum((model.el[i] * model.rat[i]) for i in model.c)
    pass


##  el total de creditos de las clases escogidas debe ser menor al LIMITE_CREDITOS
def limit_credits_rule(model: ConcreteModel):    
    return sum((model.cr[i]*model.el[i]) for i in model.c) <= LIMITE_CREDITOS



## indica que el total de cr ́editos de las clases escogidas debe ser mayor a MINIMO_CREDITOS
def set_minimum_credits_rule(model: ConcreteModel):
    return sum((model.cr[i]*model.el[i]) for i in model.c) >= MINIMO_CREDITOS


## indica que dos cursos escogidos no pueden ser de la misma seccion
def allow_one_instance_of_section_rule(model: ConcreteModel, j):
    return sum((model.el[i] * model.p[j, i]) for i in model.c) >= 1



model.objective_rule = Objective(rule=objective_rule, sense=maximize)
model.limit_credits_rule = Constraint(rule=limit_credits_rule)
model.set_minimum_credits_rule = Constraint(rule=set_minimum_credits_rule)
model.allow_one_instance_of_section = Constraint(model.s, rule=allow_one_instance_of_section_rule)


solver = SolverFactory("glpk")
solver.solve(model)

print("Materias seleccionadas:")

for i in model.el:
    if value(model.el[i]) == 1:
        print(f"Seccion {i} ha sido seleccionado con un rating de {model.rat[i]} y creditos {model.cr[i]}")
