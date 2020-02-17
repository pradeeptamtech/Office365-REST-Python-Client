from office365.runtime.client_query import UpdateEntityQuery, DeleteEntityQuery, ServiceOperationQuery
from office365.runtime.resource_path import ResourcePath
from office365.runtime.resource_path_service_operation import ResourcePathServiceOperation
from office365.runtime.utilities.http_method import HttpMethod
from office365.sharepoint.securable_object import SecurableObject


class ListItem(SecurableObject):
    """ListItem resource"""

    def update(self):
        """Update the list item."""
        qry = UpdateEntityQuery(self)
        self.context.add_query(qry)

    def validate_update_listItem(self, form_values, new_document_update):
        """Validates and sets the values of the specified collection of fields for the list item."""
        qry = ServiceOperationQuery(self,
                                    "validateUpdateListItem",
                                    None,
                                    {
                                        "formValues": form_values,
                                        "bNewDocumentUpdate": new_document_update,
                                    })
        self.context.add_query(qry)

    def system_update(self):
        """Update the list item."""
        qry = ServiceOperationQuery(self,
                                    "systemUpdate")
        self.context.add_query(qry)

    def update_overwrite_version(self):
        """Update the list item."""
        qry = ServiceOperationQuery(self,
                                    HttpMethod.Post,
                                    "updateOverwriteVersion")
        self.context.add_query(qry)

    def delete_object(self):
        """Deletes the list."""
        qry = DeleteEntityQuery(self)
        self.context.add_query(qry)

    @property
    def parentList(self):
        """Get parent List"""
        if self.is_property_available("ParentList"):
            return self.properties["ParentList"]
        else:
            from office365.sharepoint.list import List
            return List(self.context, ResourcePath("ParentList", self.resourcePath))

    @property
    def file(self):
        """Get file"""
        if self.is_property_available("File"):
            return self.properties["File"]
        else:
            from office365.sharepoint.file import File
            return File(self.context, ResourcePath("File", self.resourcePath))

    @property
    def folder(self):
        """Get folder"""
        if self.is_property_available("Folder"):
            return self.properties["Folder"]
        else:
            from office365.sharepoint.folder import Folder
            return Folder(self.context, ResourcePath("Folder", self.resourcePath))

    @property
    def attachmentFiles(self):
        """Get attachment files"""
        if self.is_property_available('AttachmentFiles'):
            return self.properties["AttachmentFiles"]
        else:
            from office365.sharepoint.attachmentfile_collection import AttachmentfileCollection
            return AttachmentfileCollection(self.context,
                                            ResourcePath("AttachmentFiles", self.resourcePath))

    def set_property(self, name, value, serializable=True):
        super(ListItem, self).set_property(name, value, serializable)
        # fallback: create a new resource path
        if name == "Id" and self._resource_path is None:
            self._resource_path = ResourcePathServiceOperation(
                "getItemById", [value], self._parent_collection.resourcePath)
