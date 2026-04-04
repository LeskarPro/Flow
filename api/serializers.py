from rest_framework import serializers
from transactions.models import Transaction, Tag
from categories.models import Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class TransactionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    # Write-only FK fields for creating/updating
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False,
    )
    formatted_amount = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'title', 'amount', 'formatted_amount',
            'date', 'type', 'category', 'category_id',
            'description', 'tags', 'tag_ids', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'formatted_amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value

    def validate(self, data):
        if data.get('type') == 'expense' and not data.get('category'):
            raise serializers.ValidationError(
                {'category_id': 'Expense transactions must have a category.'}
            )
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        transaction = Transaction.objects.create(**validated_data)
        transaction.tags.set(tags)
        return transaction

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
