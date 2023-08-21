from django.apps import AppConfig


class MovieConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie'


        # def validate(self,data):
        #     print(data,'111111111111111111111111')
        #     if data:
        #         Username = data
        #         regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')

        #         if len(Username)>100:
        #             raise serializers.ValidationError('Username must be less than 100 chars')
                
        #         # if not regex.search(Username)==None:
        #         #     raise serializers.ValidationError('Username cannot contain special character') 
            
        #     return data