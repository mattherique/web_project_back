from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST
)
from rest_framework import permissions
from .models import Usuarios, EstoqueItem, ItensUsuario
from .serializers import UsuariosSerializer, EstoqueItemSerializer, ItensUsuarioSerializer

from rest_framework.decorators import api_view

from hashlib import sha256
# Create your views here.

@api_view(["POST"])
def register_users(request):
    try:
        
        params = request.data

        password = sha256(params["password"].encode('utf-8')).hexdigest()

        new_user = Usuarios(
            nome=params["name"],
            email=params["email"],
            senha=password
        )

        new_user.save()

        return Response(
            {
                "status": "Success",
                "message": "Usuário registrado com sucesso"
            }, status=HTTP_200_OK
        )
    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao registrar usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
def list_users(request):
    try:

        users = Usuarios.objects.all()

        serializer = UsuariosSerializer(users, many=True)

        return Response(
            {
                "status": "Success",
                "message": "Usuários listados com sucesso",
                "users": serializer.data
            }, status=HTTP_200_OK
        )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao listar usuários"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def login(request):
    try:
        
        params = request.data

        user = Usuarios.objects.get(email=params["email"])

        password = sha256(params["password"].encode('utf-8')).hexdigest()

        if user.senha == password:
            return Response(
                {
                    "status": "Success",
                    "message": "Login efetuado com sucesso!"
                }, status=HTTP_200_OK
            )

        else:
            return Response(
                {
                    "status": "Error",
                    "message": "Erro ao realizar login"
                }, status=HTTP_400_BAD_REQUEST
            )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao registrar usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def register_item(request):
    try:
        
        params = request.data

        item = EstoqueItem(
            nome=params["item_name"],
            quantidade=params["item_amount"]
        )

        item.save()

        return Response(
            {
                "status": "Success",
                "message": "Login efetuado com sucesso!"
            }, status=HTTP_200_OK
        )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao registrar usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
def list_itens(request):
    try:
        
        params = request.query_params

        itens = EstoqueItem.objects.all()

        serializer = EstoqueItemSerializer(itens, many=True)

        return Response(
            {
                "status": "Success",
                "message": "Login efetuado com sucesso!",
                "itens": serializer.data
            }, status=HTTP_200_OK
        )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao registrar usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def register_user_item(request):
    try:
        
        params = request.data

        new_item = ItensUsuario(
            item_estoque_id=params["itemId"],
            usuario_id=params["user"],
            quantidade=params["itemAmount"]
        )

        new_item.save()

        return Response(
            {
                "status": "Success",
                "message": "Item registrado ao usuário com sucesso!"
            }, status=HTTP_200_OK
        )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao registrar item ao usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
def list_user_itens(request):
    try:
        
        params = request.query_params

        if "fist_date" in params or "last_date" in params:
            itens = ItensUsuario.objects.filter(usuario_id=params["user"], data_entrega__gte=params["first_date"], data_entrega__lte=params["last_date"])
        else:
            itens = ItensUsuario.objects.filter(usuario_id=params["user"])

        serializer = ItensUsuarioSerializer(itens, many=True)

        return Response(
            {
                "status": "Success",
                "message": "Itens do usuário listados com sucesso!",
                "itens": serializer.data
            }, status=HTTP_200_OK
        )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao listar itens do usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

def remove_leading_zeros(value):
    # Remove leading zeros from the value
    if type(value) == type('a'):
        return str(value.lstrip('0'))

    return '0'
    
@api_view(["POST"])
def generate_excel(request):

    try:
        import pandas as pd
        import io
        from django.http import HttpResponse

       # Load data from uploaded files
        df1 = pd.read_excel(request.FILES["client"], dtype={'Cod Cliente RM': str})
        df2 = pd.read_excel(request.FILES["base_warning"], dtype={'Código do Cliente SAP': str})
        
        df2['Código do Cliente SAP'] = df2['Código do Cliente SAP'].apply(remove_leading_zeros)
        
        # Create separate dataframes based on 'Alerta' column
        dfs = {}    
        for alerta, group in df1.groupby('Alerta'):
            dfs[alerta] = group

        # Merge each separate dataframe with the second dataframe
        merged_dfs = {}
        for alerta, df in dfs.items():
            merged_dfs[alerta] = pd.merge(df, df2, left_on='Cod Cliente RM', right_on='Código do Cliente SAP', how='inner')

        # Create Excel writer object
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        # Write each merged dataframe to a separate sheet
        for alerta, df_merged in merged_dfs.items():
            sheet_name = f'{alerta}'  # Name sheet based on alerta value
            # Select desired columns
            df_final = df_merged[['Fabricante', 'Código Equipamento Telemetria','Código do Cliente SAP', 'CódigoCliente SAP Recebedor', 'Razão Social / Nome do cliente', 'Nome Fantasia / Apelido *', 'Rua de entrega', 'Cidade de entrega', 'Bairro de Entrega', 'UF *', 'DDD e Telefone', 'Proprietário da conta', 'Email Proprietário']]
            df_final.to_excel(writer, sheet_name=sheet_name, index=False)

            workbook  = writer.book
            worksheet = writer.sheets[sheet_name]

            number_format = workbook.add_format({'align': 'center', 'bold': True})
            worksheet.set_column('B:B', 25, number_format)

            for i, col in enumerate(df_final.columns):
                # Find the maximum length of the column content
                column_len = max(df_final[col].astype(str).map(len).max(), len(col))
                # Set the column width based on the maximum length
                worksheet.set_column(i, i, column_len)

        writer.close()  # Close the writer to release resources

        # Create HTTP response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=nova_planilha.xlsx'
        output.seek(0)
        response.write(output.getvalue())

        return response

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao gerar excel"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )