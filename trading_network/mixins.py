
class RepresentationMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status_link'] = instance.get_status_link_display()
        return representation
