from rest_framework.parsers import FormParser
from rest_framework.generics import CreateAPIView
from .models import Warehouse, ProductMaterial, Product
from rest_framework.response import Response
from .serializers import MySerializer


class MyApiView(CreateAPIView):
    serializer_class = MySerializer
    parser_classes = (FormParser,)

    def post(self, request):
        serializer = MySerializer(data=request.data)
        if serializer.is_valid():
            product_name = request.data.get('product_name')
            product_qty = int(request.data.get('quantity'))

            materials_name = ProductMaterial.objects.filter(product__name__exact=product_name)
            my_dict = {}
            for obj in materials_name:
                my_dict[obj.material.name] = product_qty * obj.quantity

            product_materials = {
                f"{product_name}": my_dict
            }
            # print(product_materials)

            product_materials = {
                'Koylak': {'Mato': 24, 'Tugma': 150, 'Ip': 300},
                'Shim': {'Mato': 28, 'Ip': 300, 'Zamok': 20}}

            warehouse_list = [
                {'id': 1, 'material': 'Mato', 'remainder': 12, 'price': 1500},
                {'id': 2, 'material': 'Mato', 'remainder': 200, 'price': 1600},
                {'id': 3, 'material': 'Ip', 'remainder': 40, 'price': 500},
                {'id': 4, 'material': 'Ip', 'remainder': 300, 'price': 550},
                {'id': 5, 'material': 'Tugma', 'remainder': 500, 'price': 300},
                {'id': 6, 'material': 'Zamok', 'remainder': 1000, 'price': 2000}
            ]

            result = []
            for product_name, material_quantities in product_materials.items():
                product_result = {
                    'product_name': product_name,
                    'product_qty': product_qty,
                    'product_materials': []
                }

                allocated_ids = set()
                for material_name, required_quantity in material_quantities.items():
                    remaining_quantity = required_quantity
                    for warehouse in warehouse_list:
                        if warehouse['material'] == material_name and warehouse['remainder'] >= remaining_quantity:
                            allocated_ids.add(warehouse['id'])
                            product_result['product_materials'].append({
                                'warehouse_id': warehouse['id'],
                                'material_name': material_name,
                                'qty': remaining_quantity,
                                'price': warehouse['price']
                            })
                            warehouse['remainder'] -= remaining_quantity
                            remaining_quantity = 0
                        elif warehouse['material'] == material_name and warehouse['remainder'] > 0:
                            allocated_quantity = min(remaining_quantity, warehouse['remainder'])
                            allocated_ids.add(warehouse['id'])
                            product_result['product_materials'].append({
                                'warehouse_id': warehouse['id'],
                                'material_name': material_name,
                                'qty': allocated_quantity,
                                'price': warehouse['price']
                            })
                            warehouse['remainder'] -= allocated_quantity
                            remaining_quantity -= allocated_quantity
                        if remaining_quantity == 0:
                            break
                    if remaining_quantity > 0:
                        product_result['product_materials'].append({
                            'warehouse_id': None,
                            'material_name': material_name,
                            'qty': remaining_quantity,
                            'price': None
                        })
                for warehouse in warehouse_list:
                    if warehouse['id'] in allocated_ids:
                        warehouse['remainder'] = max(0, warehouse['remainder'])
                result.append(product_result)

            return Response({'result': result})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)