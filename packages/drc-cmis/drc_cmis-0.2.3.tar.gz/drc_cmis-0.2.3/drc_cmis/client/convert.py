import base64
import logging
from datetime import datetime

from django.conf import settings
from django.urls import reverse

from .mapper import reverse_mapper

logger = logging.getLogger(__name__)


def make_enkelvoudiginformatieobject_dataclass(cmis_doc, dataclass, skip_deleted=False):
    properties = cmis_doc.getProperties()

    if properties.get('drc:document__verwijderd') and not skip_deleted:
        # Return None if document is deleted.
        return None

    try:
        inhoud = base64.b64encode(cmis_doc.getContentStream().read()).decode("utf-8")
    except AssertionError:
        return None
    else:
        logger.error(properties)
        cmis_id = properties.get("cmis:versionSeriesId").split("/")[-1]
        path = reverse('enkelvoudiginformatieobjecten-detail', kwargs={'version': '1', 'uuid': cmis_id})
        url = f"{settings.HOST_URL}{path}"
        download_url = f"{settings.HOST_URL}{reverse('cmis:cmis_download', kwargs={'uuid': cmis_id})}"

        obj_dict = {reverse_mapper(key): value for key, value in properties.items() if reverse_mapper(key)}
        # remove verwijderd
        del obj_dict["verwijderd"]

        # Correct datetimes to dates
        for key, value in obj_dict.items():
            if isinstance(value, datetime):
                obj_dict[key] = value.date()

        # These values are not in alfresco
        obj_dict["url"] = url
        obj_dict["inhoud"] = download_url
        obj_dict["bestandsomvang"] = len(inhoud)
        return dataclass(**obj_dict)


def make_objectinformatieobject_dataclass(cmis_doc, dataclass):
    properties = cmis_doc.getProperties()

    obj_dict = {
        reverse_mapper(key, "connection"): value
        for key, value in properties.items()
        if reverse_mapper(key, "connection")
    }

    cmis_id = properties.get("cmis:versionSeriesId").split("/")[-1]
    url = "{}{}".format(
        settings.HOST_URL, reverse("objectinformatieobjecten-detail", kwargs={"version": "1", "uuid": cmis_id})
    )
    eio_url = "{}{}".format(
        settings.HOST_URL, reverse("enkelvoudiginformatieobjecten-detail", kwargs={"version": "1", "uuid": cmis_id})
    )

    obj_dict["url"] = url
    obj_dict["informatieobject"] = eio_url

    return dataclass(**obj_dict)
