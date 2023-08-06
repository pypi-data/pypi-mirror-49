const sketchpad_input = {
  html: `
    <div class="sketch_tools">
      <div id="brush_1" size="8" class="brush"></div>
      <div id="brush_2" size="16" class="brush selected"></div>
      <div id="brush_3" size="24" class="brush"></div>
    </div>
    <div class="view_holders">
      <div class="saliency_holder hide">
        <canvas class="saliency"></canvas>
      </div>
      <div class="canvas_holder">
        <canvas id="canvas"></canvas>
      </div>
    </div>`,
  init: function() {
    var io = this;
    var dimension = Math.min(this.target.find(".canvas_holder").width(),
        this.target.find(".canvas_holder").height()) - 2 // dimension - border
    var id = this.id;
    this.sketchpad = new Sketchpad({
      element: '.interface[interface_id=' + id + '] .canvas_holder canvas',
      width: dimension,
      height: dimension
    });
    this.target.find(".saliency")
      .attr("width", dimension+"px").attr("height", dimension+"px");
    this.sketchpad.penSize = this.target.find(".brush.selected").attr("size");
    this.canvas = this.target.find('.canvas_holder canvas')[0];
    this.context = this.canvas.getContext("2d");
    this.target.find(".brush").click(function (e) {
      io.target.find(".brush").removeClass("selected");
      $(this).addClass("selected");
      io.sketchpad.penSize = $(this).attr("size");
    })
  },
  submit: function() {
    var dataURL = this.canvas.toDataURL("image/png");
    this.io_master.input(this.id, dataURL);
  },
  output: function(data) {
    this.target.find(".saliency_holder").removeClass("hide");
    var ctx = this.target.find(".saliency")[0].getContext('2d');
    let dimension = this.target.find(".saliency").width();
    console.log(data, dimension, dimension);
    paintSaliency(data, dimension, dimension, ctx);
  },
  clear: function() {
    this.context.clearRect(0, 0, this.context.canvas.width, this.context.
        canvas.height);
    this.target.find(".saliency_holder").addClass("hide");
  },
  renderFeatured: function(data) {
    return `<img src=${data}>`;
  },
  loadFeatured: function(data) {
    let ctx = $(".canvas_holder canvas")[0].getContext("2d");
    var img = new Image;
    let dimension = this.target.find(".canvas_holder canvas").width();
    img.onload = function(){
      ctx.drawImage(img,0,0,dimension,dimension);
    };
    img.src = data;
  }
}
