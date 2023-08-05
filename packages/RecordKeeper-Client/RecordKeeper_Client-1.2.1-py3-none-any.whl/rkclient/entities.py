from uuid import UUID
from typing import Dict, Optional, List


"""
PEM and Artifact

Both are used by objects constructed by RKClient in memory,
and for objects constructed from http responses from Receiver.

ADR 2 - naming of member variables using PascalCase

"""


class Artifact:

    def __init__(self,
                 id: UUID,
                 type: str,
                 properties: Dict[str, str],
                 solely_id: bool = False
                 ):
        self.ID = id
        self.Type = type
        self.Properties = properties
        self.CreatedAt = None
        self.TaxonomyFiles: Optional[Dict] = None
        self.SolelyID = solely_id

    def add_taxonomy_file(self, file_id: UUID, content: str):
        if self.TaxonomyFiles is None:
            self.TaxonomyFiles = {}
        self.TaxonomyFiles[file_id.hex] = content

    def __str__(self):
        if self.SolelyID:
            return self.ID.hex
        return f"Artifact({self.ID.hex}, {self.Type}, {self.Properties}, {self.CreatedAt})"

    def __repr__(self):
        return self.__str__()


class PEM:

    def __init__(self,
                 id: UUID,
                 type: str,
                 predecessor_id: Optional[UUID],
                 emitter_id: UUID,
                 timestamp_client: str):
        self.ID = id
        self.Type = type
        self.Predecessor = predecessor_id
        self.Emitter = emitter_id
        self.TimestampClient = timestamp_client  # UTC time in format YYYY-MM-DD HH:MM:SS
        self.UsesArtifacts: List[Artifact] = []
        self.ProducesArtifacts: List[Artifact] = []
        self.TimestampReceived = ''
        self.Properties: dict = {}
        self.Version = '1.0.0'
        self.User = ''
        self.Tag = ''
        self.TagNamespace = ''

    def add_uses_artifact(self, art: Artifact):
        self.UsesArtifacts.append(art)

    def add_produces_artifact(self, art: Artifact):
        self.ProducesArtifacts.append(art)

    def __str__(self):
        return f"PEM({self.ID.hex}, {self.Type}, {self.Predecessor}, {self.Properties}, {self.TimestampClient}, " \
               f"uses: {self.UsesArtifacts}, produces: {self.ProducesArtifacts})"

    def __repr__(self):
        return self.__str__()
