from flask_dojos_ninjas.config.mysqlconnection import connectToMySQL

# modelar la clase después de la tabla dojos de nuestra base de datos
class Dojo:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de usuarioscr
        dojos = []
        # Iterar sobre los resultados de la base de datos y crear instancias de dojos con cls
        for dojo in results:
            dojos.append( cls(dojo) )
        return dojos

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_by_id(cls,id):
        #armar la consulta con cadenas f
        query = f"SELECT * FROM dojos where id = %(id)s;"
        #armar el diccionario data con solo el campo id
        data = { 'id' : id }
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)
        #devolver el primerl registro de los resultados si resultados devuelve algo sino que devuelva None
        return cls(results[0]) if len(results) > 0 else None


    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_by_name_like(cls,name):
        #armar la consulta con cadenas f
        query = f"SELECT * FROM dojos where name like %('%'+name+'%')s;"
        #armar el diccionario data con solo parte del campo name usando like
        data = { 'name' : name }
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)
        # crear una lista vacía para agregar nuestras instancias de dojos
        dojos = []
        # Iterar sobre los resultados de la base de datos y crear instancias de dojos con cls
        for dojo in results:
            dojos.append( cls(dojo) )
        return dojos

    @classmethod
    def get_ninjas_by_id(cls,id):
        #armar la consulta con cadenas f
        #query = f"SELECT * FROM dojos d left join ninjas n on d.id = n.dojo_id where d.id = %(id)s;"

        query = f"SELECT " + "d.id as d_id, d.name as d_name, n.id as nid, n.first_name as n_first_name,"
        query += "n.last_name as n_last_name, n.age as n_age, n.created_at as n_created_at, n.updated_at as n_updated_at"
        query+= "FROM dojos d left join ninjas n on d.id = n.dojo_id where d.id = %(id)s;"

        #armar el diccionario data con solo el campo id
        data = { 'id' : id }
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)
        # crear una lista vacía para agregar nuestras instancias de dojos
        ninjas_dojo = []
        # Iterar sobre los resultados de la base de datos y crear instancias de dojos con cls
        for dojo in results:
            ninjas_dojo.append( cls(dojo) )
        return ninjas_dojo


    @classmethod
    def save(cls, data):
        query = f"INSERT INTO dojos (name , created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"
        # data es un diccionario que se pasará al método de guardar desde server.py
        dojo_id = connectToMySQL('flask_mysql_coding_dojo').query_db( query, data )
        return dojo_id



    @classmethod
    def update(cls, data):
        query = f"UPDATE dojos SET name = %(name)s , updated_at = NOW() WHERE id = %(id)s;"
        # data es un diccionario que se pasará al método de guardar desde server.py
        return connectToMySQL('flask_mysql_coding_dojo').query_db( query, data )


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM dojos WHERE id = %(id)s;"
        data = {'id': id}

        print("ejecutando consulta de borrado",end='\n\n')
        print(query)

        resultado = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)

        return resultado
