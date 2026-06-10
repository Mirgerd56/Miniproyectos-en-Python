class TaskManager:
  def __init__(self):
    self.tasks = []
    
  
  def create_task(self, id, name, description, date, importance = 3):
    new_task = {}
    
    task_fields = ["Nombre", "Descripcion", "Finalizacion", "Importancia"]
    tasks_details = [name, description, date, importance]
    
    new_task[id] = dict(zip(task_fields, tasks_details))
    self.tasks.append(new_task)
    
    print("\nTarea Creada")
  
  
  def update_task(self, task_id, name = "", description = ""):
    def edit_task(task_id, field, new_value):
      for i in self.tasks:
        for j in i.keys():
          if j == task_id:
            i[j][field] = new_value
            
            print(f"\n{field} actualizado/a")
          else: 
            print(f"\nTarea No encontrada o el nuevo/a {field} no ingresado\n")
    
    task = {}
    if name != "":
      edit_task(task_id, "Nombre", name)
      
    if description != "":
      edit_task(task_id, "Descripcion", description)
  
  
  def complete_task(self, task_id): 
    found = False

    for task in self.tasks:
      if task_id in task:
        self.tasks.remove(task)
        found = True
        print(f"\nTarea {task_id} eliminada")
        break

    if not found:
      print("\nTarea No encontrada")
        
    
  def show_tasks(self):
    if self.tasks == []:
      print("No hay tareas. Crea una")
      
    tasks = [print(i) for i in self.tasks]

  
  def show_task(self, task_id):
    if task_id in self.tasks:
      print(task_id)
