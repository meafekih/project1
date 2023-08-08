import graphene

class FileType(graphene.Scalar):
    @staticmethod
    def serialize(value):
        return value  # Return the base64-encoded file data

    @staticmethod
    def parse_literal(node):
        return node.value  # Parse the file data from the GraphQL query

    @staticmethod
    def parse_value(value):
        return value  # Parse the file data from input variables

class Query(graphene.ObjectType):
    download_file = graphene.Field(FileType, filename=graphene.String(required=True))

    def resolve_download_file(self, info, filename):
        file_path = f'path/to/your/files/{filename}'
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                return file_data.encode('base64').decode()  # Encode as base64
        except FileNotFoundError:
            return None  # Return None or handle error accordingly



