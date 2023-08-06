def font(chart, fontsize=20):
    return (chart
            .configure_axis(labelFontSize=fontsize, titleFontSize=fontsize)
            .configure_header(labelFontSize=fontsize, titleFontSize=fontsize)
            .configure_title(fontSize=fontsize+5)
            .configure_legend(labelFontSize=fontsize, titleFontSize=fontsize))


