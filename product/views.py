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
            datas = {
                request.data.get('product_name1'): int(request.data.get('quantity1')),
                request.data.get('product_name2'): int(request.data.get('quantity2'))
            }
            product_materials = {}
            for d, v in datas.items():
                my_dict = {}
                # print(d,v)
                my_objs = ProductMaterial.objects.filter(product__name__exact=d)
                for obj in my_objs:
                    my_dict[obj.material.name] = v * obj.quantity
                my_dict['soni'] = v
                product_materials[d] = my_dict

            # print(product_materials)
            warehouse_queryset = Warehouse.objects.all()
            warehouse_list = []
            for warehouse in warehouse_queryset:
                warehouse_dict = {
                    'id': warehouse.id,
                    'material': warehouse.material.name,
                    'remainder': warehouse.remainder,
                    'price': int(warehouse.price),
                }
                warehouse_list.append(warehouse_dict)
            # print(warehouse_list)

            result = []
            for d, v in product_materials.items():
                # print(d, v)
                mylist = []

                for my_material, my_quantity in v.items():
                    # print(my_material, my_quantity)

                    for obj in warehouse_list:
                        obj_kopisi = obj.copy()

                        # print(obj)
                        if my_material == obj['material'] and my_quantity > obj['remainder']:

                            my_quantity -= obj_kopisi['remainder']
                            mylist.append(obj_kopisi)
                            obj['remainder'] = 0

                        elif my_material == obj['material'] and my_quantity <= obj['remainder']:
                            obj_kopisi['remainder'] = my_quantity
                            mylist.append(obj_kopisi)
                            obj['remainder'] -= my_quantity

                result.append({
                    "product_name": d,
                    "product_qty": v['soni'],
                    "product_materials": mylist,
                }
                )

            return Response({'result': result})
