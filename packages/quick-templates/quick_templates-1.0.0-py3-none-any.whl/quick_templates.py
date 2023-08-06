import os
class Blade():
    
    def __init__(self, template_name, file_name):
        self.template_name = template_name
        self.file_name = file_name
        f = open(self.file_name, 'w')
        f.write(f'@extends(\'{self.template_name}\') \n \n')
        f.close()

    def write(self, veriable, value):
        f = open(self.file_name, 'a')
        f.write(f'@section(\'{veriable}\') \n \t{value} \n@endsection \n \n \n')
        f.close()
        
    def delete(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.file_name)
        os.remove(path)



class Pug():
    
    def __init__(self, template_name, file_name):
        self.template_name = template_name
        self.file_name = file_name
        f = open(self.file_name, 'w')
        f.write(f'extends {self.template_name} \n \n \n')
        f.close()

    def write(self, block_name, value):
        f = open(self.file_name, 'a')
        f.write(f'block {block_name} \n\t{value} \n \n')
        f.close()

    def delete(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.file_name)
        os.remove(path)



class Twig():
    
    def __init__(self, template_name, file_name):
        self.template_name = template_name
        self.file_name = file_name
        f = open(self.file_name, 'w')
        f.write('{% extends "' + self.template_name + '" %} \n\n\n')
        f.close()

    def write(self, block_name, value):
        f = open(self.file_name, 'a')
        print (f'{block_name} this block already exists')
        f.write('{% block ' + block_name +' %} \n\t' + value +' \n{% endblock %}\n\n')
        f.close()

    def delete(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.file_name)
        os.remove(path)
