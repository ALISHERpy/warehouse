from rest_framework.parsers import FormParser
from rest_framework.generics import CreateAPIView
from .models import Warehouse, ProductMaterial, Product
from rest_framework.response import Response
from .serializers import MySerializer


class MyApiView(CreateAPIView):
    serializer_class = MySerializer
    parser_classes =(FormParser,)

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
            print(product_materials)
            # product_materials = {
            #     'Koylak': {'Mato': 24, 'Tugma': 150, 'Ip': 300},
            #     'Shim': {'Mato': 28, 'Ip': 300, 'Zamok': 20}
            # }


            result = []
            for product_name, material_quantities in product_materials.items():
                product_result = {
                    'product_name': product_name,
                    'product_qty': product_qty,
                    'product_materials': []
                }
                for material_name, required_quantity in material_quantities.items():
                    warehouse = Warehouse.objects.filter(material__name=material_name,
                                                         remainder__gte=required_quantity).first()
                    if warehouse:
                        product_result['product_materials'].append({
                            'warehouse_id': warehouse.id,
                            'material_name': material_name,
                            'qty': required_quantity,
                            'price': warehouse.price
                        })
                    else:
                        product_result['product_materials'].append({
                            'warehouse_id': None,
                            'material_name': material_name,
                            'qty': required_quantity,
                            'price': None
                        })
                result.append(product_result)

            return Response({'result': result})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

