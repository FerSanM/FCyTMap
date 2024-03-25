from django.db import models


# class Usuario(models.Model):
# idUsuario = models.IntegerField(blank=True, null=True)
# Nombre = models.CharField(max_length=15, blank=True, null=True)
# correo = models.EmailField(max_length=20, blank=True, null=True)
# password = models.CharField(max_length=20, blank=True, null=True)

# def __str__(self):
# return self.name  # Corregido el método str


class User(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo_electronico = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.id}{self.nombre}{self.apellido}"


class Facultad(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)


class Carrera(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    idFacultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.Descripcion}"

class Materia(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    idCarrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    semestre = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.descripcion} - {self.idCarrera.descripcion} - {self.semestre}"
    class Meta:
        ordering = ['descripcion']

class Docente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)


class Edificio(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)


class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    idEdificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.descripcion}-{self.idEdificio.descripcion}"



class Sala(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    idPlanta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Para latitud, máx. 9 dígitos y 6 decimales
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Para longitud, máx. 9 dígitos y 6 decimales

    def __str__(self):
        return f"{self.descripcion}-{self.latitud}-{self.longitud}"



class Actividades(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    idSala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_actividad = models.DateTimeField()
    fecha_notificacion = models.DateTimeField()

class RelacionUsuarioMateria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario}-{self.materia}"
class DiasSemana(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=25)
    def __str__(self):
        return f"{self.descripcion}"
class RelacionMateriaSala(models.Model):
    id = models.AutoField(primary_key=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    dia_semana = models.ForeignKey(DiasSemana, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.materia} - {self.sala} -{self.dia_semana}: {self.hora_entrada}-{self.hora_salida})"


