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
        return f"{self.nombre} {self.apellido}"


class Facultad(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=50)


class Carrera(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    idFacultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.Descripcion}"

class Materia(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    idCarrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    Semestre = models.IntegerField()

    def __str__(self):
        return f"{self.Descripcion}{self.Semestre}"


class Docente(models.Model):
    id = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)


class Edificio(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=50)


class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    idEdificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)


class Sala(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    idPlanta = models.ForeignKey(Planta, on_delete=models.CASCADE)


class Actividades(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    idSala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_actividad = models.DateTimeField()
    fecha_notificacion = models.DateTimeField()