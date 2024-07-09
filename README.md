# Hexashop

## Descrição
Este é um projeto pessoal de uma loja virtual a ideia deste projeto é ser um dropshipping logo não há implementação de controle de estoque. Segue o [modelo relacional](https://lucid.app/lucidchart/129026bc-d414-46c6-982c-a3c2c542d2e1/view?page=0_0#) e caso queira ver uma versão rodando segue uma [demostração](http://hexashop.crabdance.com/).
Técnologias utilizada:
- Python
- Django
- PostgresSQL
- JavaScript
- Bootstrap
- HTML5 & CSS

## Por quê?
Eu e um amigo tivemos a ideia de montar uma loja virtual de dropshipping, e depois de ver as taxas cobradas pelos marketplaces eu tive a ideia de criar um sistema de ecommerce.

## Instalação

### Pré-requisitos
- Python 3.10 ou versão mais recente instalada
- PostgreSQL 16.3 ou versão mais recente instalada
- Git


### Procedimento de instalação (Linux)

```bash
git clone https://github.com/AllanSBorges/E-commerce.git

cd E-commerce

```

Crie um arquivo .env para armazenar as varáveis de ambiente.

```bash
touch .env

```

Altere o arquivo .env colocando as suas informações.
Segue o conteúdo do arquivo:

```bash
SECRET_KEY="Chave de segurança do Django"
DATABASE_ENGINE="django.db.backends.postgresql" 
DATABASE_NAME="Nome do Banco de Dados"
DATABASE_USER="Nome do usuário do Banco de Dados"
DATABASE_PASSWORD="Senha do usuário do Banco de Dado"
DATABASE_HOST="Endereço do banco de dados"
DATABASE_PORT="Porta em que o Django irá se conectar com o Banco de Dados"
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="Serviço de email como por exemplo smtp do Gmail."
EMAIL_PORT="Porta que o serviço de email irá utilizar"
EMAIL_HOST_USER="Login no serviço de email"
EMAIL_HOST_PASSWORD="Senha do Login do serviço de email"
FROM_EMAIL="E-mail que o Django usará para envio de e-mail" 
DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage'
```
 
Execute o código:
```bash
python -m venv venv

source venv/bin/activate

pip install python-dotenv

pip install -r requirements.txt

cd ecommerce

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

pyhon manage.py collectstatic
```

## Utilização

No diretório raiz execute

```bash
source venv/bin/activate

cd ecommerce 

python manage.py runserver
```
Lembrando que o servidor nativo
do Django é apenas para Desenvolvimento
para produção seria necessário configurar um servidor
web como guinicorn por exemplo.

## Contribuição

Pull requests são bem vindos, assim como sugestões de melhoria.


## Créditos

O Front-End deste projeto foi feito baseado [neste template](https://templatemo.com/tm-571-hexashop).

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
