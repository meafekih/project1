# models.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.crm.schemas.customer import Customer

@receiver(pre_save, sender=Customer)
def customer_pre_save(sender, instance, **kwargs):
    if instance.pk:
        # Get the original instance from the database
        original_instance = sender.objects.get(pk=instance.pk)
        changes = []
        for field in Customer._meta.get_fields():   
            old = getattr(original_instance, field.name)
            new = getattr(instance, field.name)
            if old != new:
                  setattr(instance, field.name, new)
                  changes.append(f"'{field.name}' changed from '{old}' to '{new}'")


        if changes:
            # Log the changes
            for change in changes:
                print(change)


@receiver(post_save, sender=Customer)
def customer_post_save(sender, instance, created, **kwargs):
    #if created:
        print('we have updated customer')
        #instance_after_save = sender.objects.get(pk=instance.pk)
        print(sender)
        print(instance.email)