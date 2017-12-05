#coding: utf-8

from django import forms
from assets.models import Idc, Server, Supplier, Service

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
        fields = ('name', 'website', 'contact', 'phone', 'email', 'comment')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_name'}),
            'website': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_website'}),
            'contact': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_contact'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control',
                       'id': 'sup_phone'}),
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
        fields = ('name', 'supplier', 'use', 'cost')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'use': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': u'请输入100字以内',
                       'rows': '5'}),
            'cost': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': u'单位(元/季度)'}),
        }
