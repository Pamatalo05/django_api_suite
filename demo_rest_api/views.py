from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})

# CLASE 1: Para GET (lista) y POST
class DemoRestApi(APIView):
    name = "Demo REST API"
    
    def get(self, request):
        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        
        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)
        
        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


# CLASE 2: Para GET (individual), PUT, PATCH y DELETE
class DemoRestApiItem(APIView):
    name = "Demo REST API Item"
    
    def get_object(self, item_id):
        """Helper para encontrar un item por ID"""
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None
    
    def get(self, request, id):
        """Obtener un item específico"""
        item = self.get_object(id)
        
        if not item:
            return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(item, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        """Reemplazar completamente un item"""
        item = self.get_object(id)
        
        if not item:
            return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validación
        if 'name' not in request.data or 'email' not in request.data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar todos los campos excepto el ID
        item['name'] = request.data['name']
        item['email'] = request.data['email']
        item['is_active'] = request.data.get('is_active', True)
        
        return Response({'message': 'Item actualizado completamente.', 'data': item}, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        """Actualizar parcialmente un item"""
        item = self.get_object(id)
        
        if not item:
            return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar solo los campos proporcionados
        if 'name' in request.data:
            item['name'] = request.data['name']
        if 'email' in request.data:
            item['email'] = request.data['email']
        if 'is_active' in request.data:
            item['is_active'] = request.data['is_active']
        
        return Response({'message': 'Item actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        """Eliminar lógicamente un item"""
        item = self.get_object(id)
        
        if not item:
            return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Eliminación lógica
        item['is_active'] = False
        
        return Response({'message': 'Item eliminado exitosamente.', 'data': item}, status=status.HTTP_200_OK)