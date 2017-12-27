#coding: utf-8

from django import forms
from assets.models import Idc, Server, Supplier, Service, Requisition

class IdcForm(forms.ModelForm):
    class Meta:
        model = Idc
        fields = ('name', 'address', 'type', 'bandwidth', 'contact', 'phone', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'bandwidth': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'pattern': '.+@.+\.[a-zA-Z]{2,4}$'}),
            #'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date', 'value': '1997-01-01'}),
            #'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date', 'value': '1997-01-01'}),
            #'cost': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ('ip', 'idc', 'cabinet', 'position', 'cost', 'use')
        widgets = {
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'idc': forms.Select(attrs={'class': 'form-control'}),
            'cabinet': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': u'单位(元/季度)'}),
            'use': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': u'请输入100字以内',
                       'rows': '5'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'website', 'business', 'bus_phone', 'technical', 'tec_phone', 'contract', 'email', 'comment')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_name'}),
            'website': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_website'}),
            'business': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_business'}),
            'bus_phone': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_bus_phone'}),
            'technical': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_technical'}),
            'tec_phone': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_tec_phone'}),
            'contract': forms.FileInput(
                attrs={'class': 'form-control',
                       'id': 'sup_contract'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control',
                       'id': 'sup_email'}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control',
                       'id': 'sup_comment',
                       'placeholder': u'请输入100字以内',
                       'rows': '5'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'supplier', 'use', 'backstage', 'cost')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'use': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': u'请输入100字以内',
                       'rows': '5'}),
            'backstage': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': u'单位(元/季度)'}),
        }

class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ('payment', 'cost', 'unit', 'end_date', 'comment')
        widgets = {
            'payment': forms.Select(
                attrs={'class': 'form-control',
                       'id': 'id_payment'}),
            'cost': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'id_cost'}),
            'unit': forms.Select(
                attrs={'class': 'form-control',
                       'id': 'id_unit'}),
            'end_date': forms.DateInput(
                attrs={'class': 'form-control',
                       'id': 'id_end_date',
                       'readonly': True}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control',
                       'id': 'id_comment',
                       'placeholder': u'请输入100字以内',
                       'rows': '5'}),
        }
