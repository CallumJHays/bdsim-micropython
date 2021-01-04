
def dotfile(self, file):
    """
    Write a GraphViz dot file representing the network.

    :param file: Name of file to write to
    :type file: str

    The file can be processed using neato or dot::

        % dot -Tpng -o out.png dotfile.dot

    """
    with open(file, 'w') as file:

        header = r"""digraph G {

    graph [splines=ortho, rankdir=LR]
    node [shape=box]

    """
        file.write(header)
        # add the blocks
        for b in self.blocklist:
            options = []
            if isinstance(b, SourceBlock):
                options.append("shape=box3d")
            elif isinstance(b, SinkBlock):
                options.append("shape=folder")
            elif isinstance(b, FunctionBlock):
                if isinstance(b, Gain):
                    options.append("shape=triangle")
                    options.append("orientation=-90")
                    options.append('label="{:g}"'.format(b.gain))
                elif isinstance(b, Sum):
                    options.append("shape=point")
            elif isinstance(b, TransferBlock):
                options.append("shape=component")
            if b.pos is not None:
                options.append('pos="{:g},{:g}!"'.format(
                    b.pos[0], b.pos[1]))
            options.append(
                'xlabel=<<BR/><FONT POINT-SIZE="8" COLOR="blue">{:s}</FONT>>'
                .format(b.type))
            file.write('\t"{:s}" [{:s}]\n'.format(b.name,
                                                  ', '.join(options)))

        # add the wires
        for w in self.wirelist:
            options = []
            # options.append('xlabel="{:s}"'.format(w.name))
            if isinstance(w.end.block, Sum):
                options.append('headlabel="{:s} "'.format(
                    w.end.block.signs[w.end.port]))
            file.write('\t"{:s}" -> "{:s}" [{:s}]\n'.format(
                w.start.block.name, w.end.block.name, ', '.join(options)))

        file.write('}\n')
