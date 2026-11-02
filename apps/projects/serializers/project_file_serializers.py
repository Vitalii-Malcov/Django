from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.projects.models import ProjectFile
from apps.projects.utils.upload_file_helpers import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    check_extension,
    check_file_size,
    create_file_path,
    save_file,
)


class AllProjectFilesSerializer(ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ('id', 'file_name', 'projects')


class CreateProjectFileSerializer(ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ('file_name',)

    def validate_file_name(self, value: str) -> str:
        if not value.isascii():
            raise serializers.ValidationError("Please, provide a valid file name.")
        if not check_extension(value):
            raise serializers.ValidationError(f"Valid file extensions: {ALLOWED_EXTENSIONS}")
        return value

    def create(self, validated_data):
        raw_file = self.context.get('raw_file')
        if not check_file_size(raw_file):
            raise serializers.ValidationError(f"File size is too large ({MAX_FILE_SIZE_MB} MB as maximum).")
        file_path = create_file_path(validated_data['file_name'])
        save_file(file_path, raw_file)
        validated_data['file'] = file_path
        return ProjectFile.objects.create(**validated_data)
