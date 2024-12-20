from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class InvCab(models.Model):
    idInventario = models.BigAutoField(primary_key=True)  # Cambiado a BigAutoField para autoincrementar
    store = models.CharField(max_length=3)
    nota_inv = models.CharField(max_length=100, blank=True, null=True)
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con User
    estado = models.IntegerField(default=0)
    estado_conteo = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventario {self.idInventario} - Tienda {self.store}"

class InvConteo(models.Model):
    idInventario = models.ForeignKey(InvCab, on_delete=models.CASCADE)  # Relación con InvCab
    zona = models.IntegerField()
    cod_plano = models.IntegerField()
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Conteo para Inv {self.idInventario.idInventario} - Zona {self.zona}"

class InvDet(models.Model):
    id = models.AutoField(primary_key=True)
    idInventario = models.ForeignKey(InvCab, on_delete=models.CASCADE)  # Relación con InvCab
    zona = models.IntegerField()
    sku = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    username = models.CharField(max_length=21)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Detalle de Inv {self.idInventario.idInventario} - SKU {self.sku}"

class Datos(models.Model):
    id = models.AutoField(primary_key=True)  # Asegúrate de que `id` sea una clave primaria
    posicion = models.IntegerField(default=0)
    nombre_tienda = models.CharField(max_length=100)
    m2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    correo = models.EmailField(max_length=100)
    usuario_pc = models.CharField(max_length=100)
    clave_pc = models.CharField(max_length=100)
    nombre_pc = models.CharField(max_length=100)
    nombre_anyDesk = models.CharField(max_length=50, null=True, blank=True)
    direccion_ip = models.GenericIPAddressField()
    centro_costo = models.CharField(max_length=6)
    supervisor = models.CharField(max_length=20)
    codSii = models.TextField()
    almacen = models.CharField(max_length=4)
    codSAP = models.CharField(max_length=5)
    caja = models.IntegerField()
    ppl_epos = models.CharField(max_length=2)
    rtpro = models.BooleanField(default=False)  # tinyint(4) se puede representar como BooleanField
    vyv_pos = models.BooleanField(default=False)  # tinyint(1) se puede representar como BooleanField
    tel = models.CharField(max_length=32)
    cel = models.CharField(max_length=32)
    numero_rtpro = models.CharField(max_length=3)
    version_plugins = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=100)
    activo = models.BooleanField()
    servidor = models.BooleanField(null=True, blank=True)  # tinyint(1) puede ser null
    marca_tienda = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return self.nombre_tienda

class ProductosRtpro(models.Model):
    id = models.AutoField(primary_key=True)  # Asegúrate de que `id` sea una clave primaria
    sku = models.CharField(max_length=50)  # SKU como texto
    descripcion = models.CharField(max_length=255, blank=True, null=True)  # Descripción del producto
    ventana = models.CharField(max_length=10, blank=True, null=True)  # V0, V1, ..., V10
    temp_comercial = models.CharField(max_length=50, blank=True, null=True)  # TEMP_COMERCIAL
    coleccion = models.CharField(max_length=50, blank=True, null=True)
    familia = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    talla = models.CharField(max_length=10, blank=True, null=True)
    lppv = models.IntegerField(blank=True, null=True)  
    lpmay = models.IntegerField(blank=True, null=True)  
    lpof = models.IntegerField(blank=True, null=True)  
    lpout = models.IntegerField(blank=True, null=True) 


    def __str__(self):
        return f"Detalle SKU {self.sku} - {self.descripcion}"
    
class repositorioVentas(models.Model):
    id = models.AutoField(primary_key=True)
    invc_sid = models.CharField(max_length=50)
    service_uid = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)
    createtime = models.DateField()
    channel = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle SKU {self.sku} - Folio {self.folio}"
    
class repositorioVentasTienda(models.Model):
    id = models.AutoField(primary_key=True)
    invc_sid = models.CharField(max_length=50)
    cust_sid = models.CharField(max_length=50)
    create_date = models.DateField()
    store_code = models.CharField(max_length=50)
    type_dte = models.CharField(max_length=50)
    tracking_no = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Folio {self.invc_sid} - Tienda {self.store_code}"
    
