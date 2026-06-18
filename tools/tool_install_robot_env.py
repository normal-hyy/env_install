# -*- coding: utf-8 -*-
from .base import BaseTool
from .base import PrintUtils
from .base import run_tool_file


class Tool(BaseTool):
    def __init__(self):
        self.name = "一键部署机器人环境(系统源+ROS2 Humble+rosdep+Docker)"
        self.type = BaseTool.TYPE_INSTALL
        self.author = "Codex"

    def install_robot_env(self):
        """按预设流程部署机器人环境"""
        PrintUtils.print_success("==========开始部署机器人环境==========")

        PrintUtils.print_success("==========1. 更换系统源并添加ROS源==========")
        source_tool = run_tool_file("tools.tool_config_system_source", authorun=False)
        if not source_tool.change_sys_source(clean_mode=2, source_method_code=1):
            PrintUtils.print_error("系统源配置失败，终止机器人环境部署")
            return False
        if source_tool.add_ros_source(add_ros=True, selected_mirror="ustc") is False:
            PrintUtils.print_error("ROS源配置失败，终止机器人环境部署")
            return False

        PrintUtils.print_success("==========2. 安装ROS2 Humble桌面版==========")
        ros_tool = run_tool_file("tools.tool_install_ros", authorun=False)
        ros_version = ros_tool.install_ros(
            skip_system_source=True,
            selected_mirror="ustc",
            target_version_name="humble",
            install_type="desktop",
        )
        if ros_version is False:
            PrintUtils.print_error("ROS2 Humble安装失败，终止机器人环境部署")
            return False

        PrintUtils.print_success("==========3. 安装rosdep并切换中科大源==========")
        rosdep_tool = run_tool_file("tools.tool_config_rosdep", authorun=False)
        rosdep_result = rosdep_tool.install_rosdepc(
            preferred_source_name="中国科学技术大学"
        )
        if rosdep_result != 0:
            PrintUtils.print_error("rosdep安装失败，终止机器人环境部署")
            return False

        PrintUtils.print_success("==========4. 安装Docker==========")
        docker_tool = run_tool_file("tools.tool_install_docker", authorun=False)
        if docker_tool.install_docker() is False:
            PrintUtils.print_error("Docker安装失败，终止机器人环境部署")
            return False

        PrintUtils.print_success("机器人环境部署完成，已按预设完成系统源、ROS2 Humble、rosdep、Docker 安装流程")
        return True

    def run(self):
        return self.install_robot_env()
