from pclpy import pcl


class Viewer:
    BG_COLOR = (0.05, 0.25, 0.45)
    POINT_SIZE = 2

    def __init__(self, *clouds, overlay=True):
        self.clouds = clouds
        self.overlay = overlay

        self.point_xyz_random_color = False

        self.viewer = pcl.visualization.PCLVisualizer("viewer")

        if overlay:
            self.viewer.setBackgroundColor(*self.BG_COLOR, 0)
            for n, pc in enumerate(clouds, 1):
                handler = self.make_color_handler(pc, glasbey_lut_id=n)
                name = "cloud%s" % n
                self.viewer.addPointCloud(pc, handler, name, viewport=0)
                self.viewer.setPointCloudRenderingProperties(pcl.visualization.PCL_VISUALIZER_POINT_SIZE,
                                                             self.POINT_SIZE,
                                                             name)
        else:
            n_clouds = len(clouds)
            vp_width = 1 / n_clouds
            for n, pc in enumerate(clouds, 1):
                self.viewer.createViewPort((n - 1) * vp_width, 0.0, n * vp_width, 1.0, n)
                self.viewer.setBackgroundColor(*self.BG_COLOR, n)
                handler = self.make_color_handler(pc, glasbey_lut_id=n)
                name = "cloud%s" % n
                self.viewer.addPointCloud(pc, handler, name, viewport=n)
                self.viewer.setPointCloudRenderingProperties(pcl.visualization.PCL_VISUALIZER_POINT_SIZE,
                                                             self.POINT_SIZE,
                                                             name)

        self.viewer.resetCamera()
        self.viewer.addCoordinateSystem(1.0)
        self.viewer.setShowFPS(False)

    def show(self):
        while not self.viewer.wasStopped():
            self.viewer.spinOnce(50)

    def make_color_handler(self, pc, glasbey_lut_id=0):
        if isinstance(pc, pcl.PointCloud.PointXYZRGBA):
            return pcl.visualization.PointCloudColorHandlerRGBAField.PointXYZRGBA(pc)
        elif isinstance(pc, pcl.PointCloud.PointXYZRGB):
            return pcl.visualization.PointCloudColorHandlerRGBField.PointXYZRGB(pc)
        elif isinstance(pc, pcl.PointCloud.PointXYZ):
            if self.point_xyz_random_color:
                color = pcl.common.GlasbeyLUT.at(glasbey_lut_id)
                return pcl.visualization.PointCloudColorHandlerCustom.PointXYZ(pc, color.r, color.g, color.b)
            else:
                return pcl.visualization.PointCloudColorHandlerGenericField.PointXYZ(pc, "z")
        elif isinstance(pc, pcl.PointCloud.PointXYZI):
            return pcl.visualization.PointCloudColorHandlerGenericField.PointXYZI(pc, "intensity")
