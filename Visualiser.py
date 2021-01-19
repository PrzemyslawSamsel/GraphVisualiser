from Defines.Defines import *
from Defines.Labels import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.font = QFont()

        self.font_size = 15
        self.dot_size = 10
        self.bridge_size = 5
        self.label_offset = self.dot_size / 4
        self.label_height = self.font_size / 6
        self.bridge_line = pg.mkPen(color=(0, 0, 0), width=1.5, style=QtCore.Qt.SolidLine)
        # Offset for next bridges to be placed below on a specific column
        self.point_height_offset = -10
        # space between columns in graph
        self.x_offset = 30
        self.x_s = 100
        self.y_s = 100

        self.sum_radius = 5
        self.point_offset = Point(x=2, y=-2)
        self.scale_factor = -self.point_height_offset / 4
        self.sum_label = 's'
        self.input_label = 'x'
        self.out_label = 'y'

        self.font.setPixelSize(self.font_size)

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.window_size = (1000, 600)
        self.window_pos = (800, 400)

        self.setWindowTitle('MOV - Matrix Optimization Visualizer')
        self.setStyleSheet(load_stylesheet(qt_api='pyqt5'))
        self.setGeometry(*self.window_pos, *self.window_size)
        self.setFixedSize(*self.window_size)
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        self._setCentralLayout()
    #

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menuBar().addMenu("&Theme")
        self.menuBar().addMenu("&About")
        self.menu.addAction('&Exit', self.close)
    #

    def _createToolBar(self):
        tools = QToolBar()
        # Geffe = tools.addAction(Window.actions[0], self._change_lfsr3_state)
        # Geffe.setToolTip("Geffe Random Number Generator")
        # Geffe.setFont(Window.font_toolbar)
        # tools.addSeparator()
        # StopGo = tools.addAction(Window.actions[1], self._change_lfsr3_state)
        # StopGo.setToolTip("Stop&Go Random Number Generator")
        # StopGo.setFont(Window.font_toolbar)
        # tools.addSeparator()
        # Shrinking = tools.addAction(Window.actions[2], self._change_lfsr3_state)
        # Shrinking.setToolTip("Shrinking Random Number Generator")
        # Shrinking.setFont(Window.font_toolbar)
        self.addToolBar(tools)
    #

    def _createStatusBar(self):
        self._status = QStatusBar()
        self._status.showMessage("")
        self.setStatusBar(self._status)
    #

    def _setCentralLayout(self):
        grid = QGridLayout()
        centralWidget = QWidget()

        # params group defines view of all parameters to plotting graph
        def params_group():
            widgets_view = []
            # Frame that will hold horizontal buttons layout
            button_frame = QFrame()
            # Create horizontal layout
            central_grid = QGridLayout()

            # First section - equation parameters
            # Label
            eq_label = QLabel(params_lbl_eq)
            # Equation
            equation = QLineEdit()
            equation.setFixedWidth(120)
            equation.setToolTip(equation_lbl_tooltip)
            # Button to set matrices
            get_mx_button = QPushButton(set_data_lbl)
            get_mx_button.clicked.connect(self._get_data_dialog)
            get_mx_button.setToolTip(set_data_tooltip)

            # Second section - graph specific parameters
            # Label
            gr_label = QLabel(graph_params_lbl)
            # Parameter 1 - Column offset
            col_offset = QSpinBox()
            col_offset.setRange(1, 1000)
            col_offset.setValue(self.x_offset)
            col_offset_lbl = QLabel(column_offset_lbl)
            col_offset_lbl.setToolTip(column_offset_tooltip)
            # Parameter 2 - Vertical offset
            ver_offset = QSpinBox()
            ver_offset.setRange(-1000, -1)
            ver_offset.setValue(self.point_height_offset)
            ver_offset_lbl = QLabel(vertical_offset_lbl)
            ver_offset_lbl.setToolTip(vertical_offset_tooltip)
            # Parameter 3 - Bridge size
            br_size = QSpinBox()
            br_size.setRange(1, 1000)
            br_size.setValue(self.bridge_size)
            br_size_lbl = QLabel(bridge_size_lbl)
            br_size_lbl.setToolTip(bridge_size_tooltip)
            # TODO: grid enable, disable

            # Third section - fonts and labels on graph
            # Label
            fonts_label = QLabel(fonts_labels_lbl)
            # Fonts for X, Y and Sums
            labels_layout = QHBoxLayout()
            labels_frame  = QFrame()
            X_lbl = QLabel(x_label)
            Y_lbl = QLabel(y_label)
            Sum_lbl = QLabel(sum_label)

            x_text = QLineEdit()
            x_text.setFixedWidth(20)
            x_text.setText(self.input_label)

            y_text = QLineEdit()
            y_text.setFixedWidth(20)
            y_text.setText(self.out_label)

            sum_text = QLineEdit()
            sum_text.setFixedWidth(20)
            sum_text.setText(self.sum_label)

            labels_layout.addWidget(X_lbl)
            labels_layout.addWidget(x_text)
            labels_layout.addWidget(Y_lbl)
            labels_layout.addWidget(y_text)
            labels_layout.addWidget(Sum_lbl)
            labels_layout.addWidget(sum_text)
            labels_frame.setLayout(labels_layout)

            font_size = QSpinBox()
            font_size.setRange(1, 1000)
            font_size.setValue(self.font_size)
            font_size_lbl = QLabel(font_size_label)
            font_size_lbl.setToolTip(font_size_tooltip)

            # Fourth section - buttons to generate and save graphs
            # Label
            generate_section = QLabel(generate_section_label)
            # Button to generate results on graph
            generate_button = QPushButton(generate_label)
            generate_button.setFixedWidth(30)
            generate_button.clicked.connect(self.generate_button)
            generate_button.setToolTip(generate_label_tooltip)
            # Button to export results to a file
            export_button = QPushButton(export_label)
            export_button.setFixedWidth(30)
            export_button.clicked.connect(self.export_button)
            export_button.setToolTip(export_label_tooltip)

            # First section
            central_grid.addWidget(eq_label, *(0, 0))
            central_grid.addWidget(equation, *(1, 0))
            central_grid.addWidget(get_mx_button, *(1, 1))
            # Second section
            central_grid.addWidget(gr_label, *(2, 0))
            central_grid.addWidget(col_offset_lbl, *(3, 0))
            central_grid.addWidget(col_offset, *(3, 1))
            central_grid.addWidget(ver_offset_lbl, *(4, 0))
            central_grid.addWidget(ver_offset, *(4, 1))
            central_grid.addWidget(br_size_lbl, *(5, 0))
            central_grid.addWidget(br_size, *(5, 1))
            # Third section
            central_grid.addWidget(fonts_label, *(6, 0))
            central_grid.addWidget(labels_frame, *(7, 0))
            central_grid.addWidget(font_size_lbl, *(8, 0))
            central_grid.addWidget(font_size, *(8, 1))
            # Fourth section
            central_grid.addWidget(generate_section, *(9, 0))
            central_grid.addWidget(generate_button, *(10, 0))
            central_grid.addWidget(export_button, *(10, 1))

            # Add layout to frame
            button_frame.setLayout(central_grid)
            # Append frame to widgets
            widgets_view.append(button_frame)

            return widgets_view
        #

        # graphview group defines plotting window view and progress bar
        # that shows the status of computation
        def graphview_group():
            widgets_view = []
            widgets_refs = []
            verlay = QVBoxLayout()
            graph_frame = QFrame()

            graph_widget = pg.PlotWidget()
            graph_widget.setBackground('w')
            graph_widget.getPlotItem().hideAxis('bottom')
            graph_widget.getPlotItem().hideAxis('left')
            verlay.addWidget(graph_widget)
            widgets_refs.append(graph_widget)

            test_progress = QProgressBar()
            test_progress.setValue(0)
            test_progress.setTextVisible(True)
            progress_txt = "%p%".format(0)
            test_progress.setFormat(progress_txt)
            verlay.addWidget(test_progress)
            widgets_refs.append(graph_widget)

            verlay.addStretch()
            graph_frame.setLayout(verlay)
            widgets_view.append(graph_frame)
            return widgets_view, widgets_refs
        #

        # Create groups of widgets based on above functions
        gt = namedtuple("Group", ["box", "layout", "widgets", "pos"])
        groups = (gt(box=QGroupBox("Parameters"), layout=QVBoxLayout(), widgets=[], pos=(0, 0)),
                  gt(box=QGroupBox("Graph View"), layout=QVBoxLayout(), widgets=[], pos=(0, 1)))

        # define lists of widgets (groups)
        group_params = params_group()
        group_graph, graph_refs = graphview_group()

        # assign defined lists of widgets
        groups[0].widgets.extend(group_params)
        groups[1].widgets.extend(group_graph)
        # add references
        self.graphWidget, self.progressBar = graph_refs[0], graph_refs[1]

        # Assign all groups to a grid and plot them
        for g in groups:
            for w in g.widgets:
                g.layout.addWidget(w)
            g.box.setLayout(g.layout)
            grid.addWidget(g.box, *g.pos)

        # Set layouts
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)
    #

    def generate_button(self):
        main.plot_scheme(example_4[::-1], sum_matrix_index=example_4_sum_i)

    def export_button(self):
        print("OK 2")

    def _get_data_dialog(self):
        # Initial settings for dialog
        d = QDialog()
        d.setStyleSheet(load_stylesheet(qt_api='pyqt5'))
        pos = self.pos()
        d.move(pos.x() + 100, pos.y() + 200)
        d.setWindowTitle("Add data")
        d.setWindowModality(pqtc.Qt.ApplicationModal)

        # Create horizontal layout
        dialog_grid = QGridLayout()

        m1 = QLabel("M1")
        m1_button = QPushButton("Add file")
        dialog_grid.addWidget(m1, *(0,0))
        dialog_grid.addWidget(m1_button, *(0,1))

        d.setLayout(dialog_grid)
        d.exec_()

    # in case there is junction, bridge must be plotted to extend point's arm
    # x, y is just point coords
    # size is the length of arm
    # dir 1 => left, 0 => right (direction of point's arm/bridge)
    # returns => coords of the end of bridge, will be the new point
    def plot_bridge(self, bridge, label="", index=0, label_side=LABEL_LEFT):
        if label != "":
            label_item = None
            if label_side == LABEL_LEFT:
                label_item = pg.TextItem(html=label + f"<sub>{index}</sub>", anchor=(1, 1))
                label_item.setPos(bridge.left_point.x - self.label_offset, bridge.left_point.y - self.label_height)
            elif label_side == LABEL_RIGHT:
                label_item = pg.TextItem(html=label + f"<sub>{index}</sub>", anchor=(0, 1))
                label_item.setPos(bridge.right_point.x + self.label_offset, bridge.right_point.y - self.label_height)
            if label_item is not None:
                label_item.setFont(self.font)
                self.graphWidget.addItem(label_item)

        #TODO: should I add offset to these points like with labels [1,1] ??
        self.graphWidget.plot([bridge.left_point.x], [bridge.left_point.y], symbol='o', symbolSize=self.dot_size, symbolBrush="k")
        self.graphWidget.plot([bridge.left_point.x, bridge.right_point.x], [bridge.left_point.y, bridge.right_point.y], pen=self.bridge_line)
        self.graphWidget.plot([bridge.right_point.x], [bridge.right_point.y], symbol='o', symbolSize=self.dot_size, symbolBrush="k")
        return bridge
    #

    # Plot circle with symbol inside, representing specific sum
    # on both sides of circle plot bridges and return right point of right bridge
    # next_bridge => right point of previous bridge that sum will be plotted on
    # index => index of symbol plotted inside sum
    # symbol => sum symbol inside sum
    def plot_sum(self, left_bridge, index=0):
        # get starting point of circle sum and plot starting bridge
        # right_point = self.plot_bridge(left_bridge)
        # create circle, which starts in the middle of right side (coordinates of right point of left bridge)
        c_sum = CircleItem([left_bridge.right_point.x, left_bridge.right_point.y], self.sum_radius)
        # plot right bridge
        right_bridge = Bridge(Point(left_bridge.right_point.x + self.sum_radius + self.bridge_size, left_bridge.right_point.y), self.bridge_size)
        self.plot_bridge(right_bridge)

        # Add text label to sum
        l_sum = pg.TextItem(html=str(self.sum_label) + f"<sub>{index}</sub>", anchor=(1, 1))
        l_sum.setPos(left_bridge.right_point.x + self.sum_radius + self.point_offset.x, left_bridge.right_point.y + self.point_offset.y)
        l_sum.setFont(self.font)
        #

        # plot sum circle and label
        self.graphWidget.addItem(c_sum)
        self.graphWidget.addItem(l_sum)

        # return right bridge
        return right_bridge
    #

    # Plot halamards sum
    def plot_h(self, x, y, x_size, y_size):
        c1 = RectangleItem([x, y], [x_size, y_size])
        name = "H"
        index = 2

        # Add text label to h
        t_up = pg.TextItem(html=f"<b>{name}</b>" + f"<sub>{index}</sub>", anchor=(1, 1))
        t_up.setPos(x + x_size * 0.9, y + y_size / 3.5)
        t_up.setFont(self.font)
        #

        # todo: add 4 points, 2 on each side of the square

        self.graphWidget.addItem(c1)
        self.graphWidget.addItem(t_up)
    #

    # connect two points with a line
    # b_s is a (start) Bridge with start coordinates (x, y)
    # b_e is a (end) Bridge with end coordinates (x, y)
    def link_bridge(self, b_s, b_e, line_type=1):
        ln_obj = 0
        if line_type == 1:
            ln_obj = QtCore.Qt.SolidLine
        elif line_type == -1:
            ln_obj = QtCore.Qt.DashLine

        if line_type != 0:
            line = pg.mkPen(color=(0, 0, 0), width=1.5, style=ln_obj)
            self.graphWidget.plot([b_s.right_point.x, b_e.left_point.x],
                              [b_s.right_point.y, b_e.left_point.y],
                              pen=line, symbol='o', symbolSize=10, symbolBrush="k")
    #

    # Given set of input points m_in, output points m_out and x_s, y_s as starting coords
    def plot_scheme(self, mx_list, sum_matrix_index=0):
        # Length of list of matrices in equation should be at least 3. Two combinations and one sum
        assert len(mx_list) >= 3
        # Matrix index must be given (and it will never be 1st matrix, that's why 0 here)
        assert sum_matrix_index != 0

        # Create starting bridge => x0
        start_bridge = Bridge(Point(self.x_s, self.y_s), length=self.bridge_size)
        # Move to the next offset in order to draw entire second column of bridges
        start_bridge += Point(self.x_offset)

        # Adjusting height of bridge - centering
        # set offset for Y so that graph will be nicely stretched and centered
        # Do it only if matrix dimensions are not equal
        if mx_list[0].shape[0] != mx_list[0].shape[1]:
           start_bridge += Point(y=mx_list[0].shape[1] * self.scale_factor)
        # Draw second column, that input (x) column will connect to
        # Save all coordinates of bridges in a new_bridges list
        new_bridges   = list(self.set_bridges(mx_list[0].shape[0], start_bridge))

        # Secondly, iterate over input (x) points and connect each of them with specific
        # bridge they should be connected to
        # Iterate over rows (inputs)
        # Reinitialize start_bridge. This is because now the rest of bridges will be plotted and connected, one by one
        start_bridge = Bridge(Point(self.x_s, self.y_s), length=self.bridge_size)
        for pt_nr in range(mx_list[0].shape[1]):
            # Plot nth input (x) bridge and give it a label
            sb = self.plot_bridge(start_bridge, self.input_label, index=pt_nr)

            # Iterate over next column of bridges (columns)
            # Connect each input bridge which next bridge it should be connected to
            for coord in range(mx_list[0].shape[0]):
                self.link_bridge(sb, new_bridges[coord], mx_list[0][coord][pt_nr])

            # Create offset, space in Y axis so that next input (x) bridge will be plotted below
            start_bridge += Point(y=self.point_height_offset)
        #

        # set offset for next bridge - in X axis, so that new bridge will be further
        # also, set offset for Y so that graph will be nicely stretched and centered
        start_bridge = Bridge(Point(self.x_s, self.y_s), length=self.bridge_size) + Point(x=self.x_offset)
        # Next, iterate over remaining matrices in the list and for each matrix:
        # Reinitialize start point and add x offset to it. This way next bridge
        # is prepared to be plotted in next column
        # set offset for Y so that graph will be nicely stretched and centered
        # Do it only if matrix dimensions are not equal
        for i, mx in enumerate(mx_list[1:-1]):
            # Adjusting height of bridge - centering
            # Adjust height of next columns of bridges so that entire graph will
            # be nicely centered
            # (and do it only for equations that have more than 3 matrices)
            if len(mx_list) > 3:
                if i + 1 < sum_matrix_index:
                    start_bridge += Point(y=mx_list[0].shape[1] * self.scale_factor)
                if i + 1 > sum_matrix_index:
                    start_bridge += Point(y=mx_list[0].shape[1] * -self.scale_factor)
            elif len(mx_list) == 3:
                start_bridge += Point(y=mx_list[0].shape[1] * self.scale_factor)

            # Executed when sum matrix met
            if i + 1 == sum_matrix_index:
                # draw column of sums
                new_bridges = list(self.set_sums(len(mx), start_bridge))
                # right bridge of sum will be next bridge
                start_bridge = new_bridges[0]
                # Adjusting height of bridge - centering
                # add offset to bridge in order to prepare it for next column
                start_bridge += Point(y=mx_list[0].shape[1] * -self.scale_factor * 2)
            # Executed when normal matrix with combinations met
            else:
                # Reinitialize start point - just to make all points in next column start from the same Y height
                new_bridges = list(self.set_bridges(mx.shape[0], start_bridge + Point(x=self.x_offset)))
                # For each point in the current input (or just previous) column
                # connect it to the specific point in next column that it should be connected to
                if sum_matrix_index in (i, i - 1) and len(mx_list) > 3:
                    start_bridge += Point(y=mx_list[0].shape[1] * self.scale_factor * 2)

                for index, el in ndenumerate(transpose(mx)):
                    if index[1] == 0:
                        start_bridge.right_point.y += self.point_height_offset
                    self.link_bridge(start_bridge, new_bridges[index[1]], mx[index[1]][index[0]])
                start_bridge = new_bridges[0]

            # Adjusting height of bridge - centering
            if i + 1 == sum_matrix_index:
                if len(mx_list) > 3:
                    start_bridge += Point(y=mx_list[0].shape[1] * self.scale_factor * 2)
                if len(mx_list) == 3:
                    start_bridge += Point(y=mx_list[0].shape[1] * self.scale_factor)
            #
        #

        # Adjusting height of bridge - centering
        # set offset for next bridge - in X axis, so that new bridge will be further
        # also, set offset for Y so that graph will be nicely stretched and centered
        start_bridge += Point(self.x_offset)
        if mx_list[-1].shape[0] != mx_list[0].shape[1]:
            start_bridge += mx_list[0].shape[1] * -self.scale_factor
        # Draw last column of bridges that it will connect to
        last_bridges = list(self.set_bridges(mx_list[-1].shape[1], start_bridge, [self.out_label, LABEL_RIGHT]))
        #for index, el in ndenumerate(mx):
        for pt_nr in range(mx_list[-1].shape[1]):
            for coord in range(mx_list[-1].shape[0]):
                self.link_bridge(new_bridges[pt_nr], last_bridges[coord], mx_list[-1][coord][pt_nr])
    #

    # For given starting bridge, draw column of bridges, number indicated by mx_len
    def set_bridges(self, mx_len, start_bridge, params=None):
        for i in range(mx_len):
            # Plot bridge without label
            if params is None:
                self.plot_bridge(start_bridge)
            # Plot bridge with label
            else:
                self.plot_bridge(start_bridge, params[0], i, params[1])
            # yield coordinates of each bridge
            yield start_bridge
            # move downwards to draw next bridge
            start_bridge += Point(y=self.point_height_offset)
    #

    # For given starting bridge, draw column of sums, number indicated by mx_len
    def set_sums(self, mx_len, start_bridge):
        for i in range(mx_len):
            # plot sum (circle and right-side bridge) next to sum's left side bridge
            # meaning: it does not plot left bridge, only plots circle and right bridge to it
            next_bridge = self.plot_sum(start_bridge, i)
            # Add coordinates of right bridge
            yield next_bridge
            # Take vertical offset into consideration
            start_bridge += Point(y=self.point_height_offset)
    #
#


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()

    main.show()
    sys.exit(app.exec_())