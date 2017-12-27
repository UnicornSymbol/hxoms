# coding:utf-8

from __future__ import unicode_literals

from django.db import models

idc_type = (
    ('DX', u'电信'),
    ('LT', u'联通'),
    ('YD', u'移动'),
    ('ZJ', u'自建'),
)

asset_status = (
    (1, u"正常"),
    (2, u"停用"),
)

server_type = (
    (1, u"物理机"),
    (2, u"虚拟机"),
    (3, u"容器"),
)

payment = (
    (1, u"银行支付"),
    (2, u"支付宝支付"),
)

payment_status = (
    (1, u"待付款"),
    (2, u"已付款"),
    (3, u"待续费"),
    (4, u"已申请续费"),
)

approve_status = (
    (1, u"待审核"),
    (2, u"已通过"),
    (3, u"未通过"),
)

unit = (
    (1, u"人民币 CNY"),
    (2, u"港币 HKD"),
    (3, u"美金 USD"),
)

def contract_dir_path(instance, filename):
    return 'contract/{0}/{1}'.format(instance.name, filename)

# Create your models here.
class Idc(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name=u'机房名字')
    address = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'机房地址')
    type = models.CharField(choices=idc_type, max_length=20, verbose_name=u'机房类型', default='DX')
    bandwidth = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'机房带宽')
    contact = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'联系人')
    phone = models.CharField(blank=True, null=True, max_length=20, verbose_name=u'联系电话')
    email = models.EmailField(blank=True, null=True, verbose_name=u'邮箱')
    def __str__(self):
        return self.name
    __repr__ = __str__

    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = u'机房列表'

class Server(models.Model):
    ip = models.GenericIPAddressField(unique=True, verbose_name='IP')

    idc = models.ForeignKey(Idc, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u'所属机房')
    cabinet = models.CharField(blank=True,null=True,  max_length=30, verbose_name=u'机柜号')
    position = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'机器位置')

    status = models.IntegerField(choices=asset_status, blank=True, null=True, verbose_name=u'状态', default=1)
    buy_date = models.DateField(blank=True, null=True, auto_now_add=True, verbose_name=u"购买日期")
    end_date = models.DateField(null=True, blank=True, verbose_name=u'到期日期')
    cost = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"购买费用")
    use = models.TextField(blank=True, null=True, max_length=100, verbose_name=u'作用')

    def __str__(self):
        return self.ip
    __repr__ = __str__

    class Meta:
        verbose_name = u'服务器'
        verbose_name_plural = u'服务器列表'

class ServerInfo(models.Model):
    ip = models.OneToOneField(Server, verbose_name="IP")
    #other_ip = models.CharField(blank=True, null=True, max_length=100, verbose_name=u"其他IP")
    #remote_ip = models.GenericIPAddressField(blank=True ,null=True ,verbose_name=u'远控卡IP')
    hostname = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'主机名')
    hwaddr = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'MAC地址')

    manufacturer = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'厂商')
    brand = models.CharField(blank=True, null=True, max_length=20, verbose_name=u'产品型号')

    cpu = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'CPU型号')
    cpu_num = models.PositiveSmallIntegerField(verbose_name=u'CPU核数')
    memory = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'内存')
    disk = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'硬盘')

    system_type = models.CharField(blank=True, null=True, max_length=20, verbose_name=u'系统类型')
    system_version = models.CharField(blank=True, null=True, max_length=20, verbose_name=u'系统版本')
    system_arch = models.CharField(blank=True, null=True, max_length=20, verbose_name=u'系统平台')

    type = models.IntegerField(choices=server_type, blank=True, null=True, verbose_name=u'类型', default=1)
    virtual = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'虚拟环境')
    # 同一个表中，OneToOneField和ForeignKey不能同时关联同一个对象，所以这里只能关联self
    vm = models.ForeignKey("self", blank=True, null=True, on_delete=models.PROTECT, verbose_name=u'宿主机')
    sn = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'序列号')

    def __str__(self):
        return self.ip.ip
    __repr__ = __str__

    class Meta:
        verbose_name = u'服务器信息'
        verbose_name_plural = u'服务器信息列表'

class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name=u"供应商名称")
    website = models.CharField(blank=True, null=True, max_length=100,verbose_name=u"网站")
    # FileField默认会自动上传文件，不需要通过chunk操作保存
    contract = models.FileField(blank=True, null=True, upload_to=contract_dir_path, verbose_name=u"合同")
    business = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'业务联系人')
    bus_phone = models.CharField(blank=True, null=True, max_length=20, verbose_name=u'业务联系人电话')
    technical = models.CharField(blank=True, null=True, max_length=50, verbose_name=u'业务联系人')
    tec_phone = models.CharField(blank=True, null=True, max_length=20, verbose_name=u'技术联系人电话')
    email = models.EmailField(blank=True, null=True, verbose_name=u'邮箱')
    comment = models.TextField(blank=True, null=True, max_length=100, verbose_name=u'备注')

    def __str__(self):
        return self.name
    __repr__ = __str__

    class Meta:
        verbose_name = u'供应商'
        verbose_name_plural = u'供应商列表'
    

# 互联网服务资产类型，例如：adsl、域名等
class Type(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name=u'类型名称')

    def __str__(self):
        return self.name
    __repr__ = __str__

    class Meta:
        verbose_name = u'服务类型'
        verbose_name_plural = u'服务类型列表'

class Service(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name=u"服务名称")
    type = models.ForeignKey(Type, blank=True, null=True ,verbose_name=u"服务类型")
    supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"供应商")
    use = models.TextField(blank=True, null=True, max_length=100, verbose_name=u"作用")
    backstage = models.CharField(blank=True, null=True, max_length=128, verbose_name=u"后台地址")
    status = models.IntegerField(choices=asset_status, blank=True, null=True, verbose_name=u'状态', default=1)
    
    buy_date = models.DateField(blank=True, null=True, auto_now_add=True, verbose_name=u"购买日期")
    end_date = models.DateField(null=True, blank=True, verbose_name=u'到期日期')
    cost = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"购买费用")

    def __str__(self):
        return self.name
    __repr__ = __str__

    class Meta:
        verbose_name = u'服务'
        verbose_name_plural = u'服务列表'

class Requisition(models.Model):
    asset = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"资产")
    payment = models.IntegerField(choices=payment, verbose_name=u"支付方式", default=1)
    info = models.CharField(blank=True, null=True, max_length=100, verbose_name=u"支付信息")
    cost = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"申请单金额")
    unit = models.IntegerField(choices=unit, verbose_name=u'金额单位', default=1)
    payment_status = models.IntegerField(choices=payment_status, blank=True, null=True, verbose_name=u'付款状态', default=1)
    approve_status = models.IntegerField(choices=approve_status, blank=True, null=True, verbose_name=u'审批状态', default=1)
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u"创建时间")
    end_date = models.DateField(null=True, blank=True, verbose_name=u'资产截止日期')
    comment = models.TextField(blank=True, null=True, max_length=100, verbose_name=u'备注')

    class Meta:                                                                 
        verbose_name = u'申请单'                                                  
        verbose_name_plural = u'申请单列表'
