# A component of the BASEmesh pre-processing toolkit.
# Copyright (C) 2020  ETH Zürich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Algorithms allowing the retrieval of elements by location."""

from typing import Any, Dict, List, Optional

from PyQt5.QtCore import QVariant
from qgis.core import (QgsFeature, QgsField, QgsFields, QgsMeshLayer, QgsPoint,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingContext, QgsProcessingFeedback,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterMeshLayer,
                       QgsProcessingParameterVectorLayer, QgsVectorLayer,
                       QgsWkbTypes)

from ...core.mesh import Mesh
from ...types import Point2D
from .utils import parse_docstring

# pylint: disable=invalid-name


class GetNodeByLocation(QgsProcessingAlgorithm):
    """Retrieve the IDs of the closest nodes for a set of points."""

    # pylint: disable=no-self-use

    INPUT = 'INPUT'
    POINTS = 'POINTS'
    OUTPUT = 'OUTPUT'

    @classmethod
    def createInstance(cls) -> 'GetNodeByLocation':
        """Return a new copy of the algorithm."""
        return cls()

    def name(self) -> str:
        """Return the unique algorithm name."""
        return 'getnodebylocation'

    def displayName(self) -> str:
        """Return the user-facing algorithm name."""
        return 'Get mesh node by location'

    def shortHelpString(self) -> str:
        """Return a short help string for the algorithm."""
        return parse_docstring(self.__class__.__doc__)

    def initAlgorithm(
            self, configuration: Optional[Dict[str, Any]] = None) -> None:
        """Define the algorithm's inputs and outputs."""
        _ = configuration
        # Input mesh
        self.addParameter(QgsProcessingParameterMeshLayer(
            name=self.INPUT,
            description='Mesh layer'))
        # Input points
        self.addParameter(QgsProcessingParameterVectorLayer(
            name=self.POINTS,
            description='Input points',
            types=[QgsProcessing.TypeVectorPoint]))
        # Output
        self.addParameter(QgsProcessingParameterFeatureSink(
            name=self.OUTPUT,
            description='Output point layer',
            type=QgsProcessing.TypeVectorPoint))

    def processAlgorithm(self, parameters: Dict[str, Any],
                         context: QgsProcessingContext,
                         feedback: QgsProcessingFeedback) -> Dict[str, Any]:
        """Execute the algorithm using the given parameters.

        Parameters
        ----------
        parameters : Dict[str, Any]
            The parameters defined for this algorithm
        context : QgsProcessingContext
            The context in which the algorithm is run
        feedback : QgsProcessingFeedback
            The feedback object to use for status reporting

        Returns
        -------
        Dict[str, Any]
            The algorithms output parameters
        """
        input_mesh_layer: QgsMeshLayer = self.parameterAsMeshLayer(
            parameters, self.INPUT, context)
        mesh = Mesh.open(input_mesh_layer.source())
        points_layer: QgsVectorLayer = self.parameterAsVectorLayer(
            parameters, self.POINTS, context)
        fields = QgsFields()
        fields.append(QgsField('Node_ID', type=QVariant.Int))
        sink, dest_id = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields,
            geometryType=QgsWkbTypes.Point, crs=points_layer.crs())

        # Extract points
        points: List[Point2D] = []
        feature: QgsFeature
        for feature in points_layer.getFeatures():
            for vertex in feature.geometry().vertices():
                points.append((vertex.x(), vertex.y()))

        # Resolve nodes
        if mesh.nodes:
            for point in points:
                node = mesh.get_node(point)
                new_feat = QgsFeature()
                new_feat.setGeometry(QgsPoint(*point))
                new_feat.setAttributes([node.id_])
                sink.addFeature(new_feat)

        feedback.setProgress(100)
        return {self.OUTPUT: dest_id}


class GetElementByLocation(QgsProcessingAlgorithm):
    """Retrieve the IDs of the elements containing a set of points."""

    # pylint: disable=no-self-use

    INPUT = 'INPUT'
    POINTS = 'POINTS'
    OUTPUT = 'OUTPUT'

    @classmethod
    def createInstance(cls) -> 'GetElementByLocation':
        """Return a new copy of the algorithm."""
        return cls()

    def name(self) -> str:
        """Return the unique algorithm name."""
        return 'getelementbylocation'

    def displayName(self) -> str:
        """Return the user-facing algorithm name."""
        return 'Get mesh element by location'

    def shortHelpString(self) -> str:
        """Return a short help string for the algorithm."""
        return parse_docstring(self.__class__.__doc__)

    def initAlgorithm(
            self, configuration: Optional[Dict[str, Any]] = None) -> None:
        """Define the algorithm's inputs and outputs."""
        _ = configuration
        # Input mesh
        self.addParameter(QgsProcessingParameterMeshLayer(
            name=self.INPUT,
            description='Mesh layer'))
        # Input points
        self.addParameter(QgsProcessingParameterVectorLayer(
            name=self.POINTS,
            description='Input points',
            types=[QgsProcessing.TypeVectorPoint]))
        # Output
        self.addParameter(QgsProcessingParameterFeatureSink(
            name=self.OUTPUT,
            description='Output point layer',
            type=QgsProcessing.TypeVectorPoint))

    def processAlgorithm(self, parameters: Dict[str, Any],
                         context: QgsProcessingContext,
                         feedback: QgsProcessingFeedback) -> Dict[str, Any]:
        """Execute the algorithm using the given parameters.

        Parameters
        ----------
        parameters : Dict[str, Any]
            The parameters defined for this algorithm
        context : QgsProcessingContext
            The context in which the algorithm is run
        feedback : QgsProcessingFeedback
            The feedback object to use for status reporting

        Returns
        -------
        Dict[str, Any]
            The algorithms output parameters
        """
        input_mesh_layer: QgsMeshLayer = self.parameterAsMeshLayer(
            parameters, self.INPUT, context)
        mesh = Mesh.open(input_mesh_layer.source())
        points_layer: QgsVectorLayer = self.parameterAsVectorLayer(
            parameters, self.POINTS, context)
        fields = QgsFields()
        fields.append(QgsField('Element_ID', type=QVariant.Int))
        sink, dest_id = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields,
            geometryType=QgsWkbTypes.Point, crs=points_layer.crs())

        # Extract points
        points: List[Point2D] = []
        feature: QgsFeature
        for feature in points_layer.getFeatures():
            for vertex in feature.geometry().vertices():
                points.append((vertex.x(), vertex.y()))

        # Resolve elements
        if mesh.elements:
            for point in points:
                element = mesh.get_element(point)
                new_feat = QgsFeature()
                new_feat.setGeometry(QgsPoint(*point))
                new_feat.setAttributes([element.id_])
                sink.addFeature(new_feat)

        feedback.setProgress(100)
        return {self.OUTPUT: dest_id}
