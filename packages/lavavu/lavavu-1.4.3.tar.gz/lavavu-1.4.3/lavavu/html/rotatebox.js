//RotateBox rotation widget in WebGL
//TODO: create class heirarchy to clean up duplicate code in this with drawbox.js and draw.js
function initRotateBox(el) {
  //console.log("INITBOX: " + el.id);
  var canvas = document.createElement("canvas");
  if (!el) el = document.body.firstChild;
  canvas.id = "canvas_" + el.id;
  canvas.imgtarget = el
  el.parentElement.appendChild(canvas);
  canvas.style.cssText = "position: absolute; width: 100%; height: 100%; margin: 0px; padding: 0px; top: 0; left: 0; bottom: 0; right: 0; z-index: 11; border: none;"
  var viewer = new RotateBoxViewer(canvas);

  //Canvas event handling
  canvas.mouse = new Mouse(canvas, new MouseEventHandler(canvasRotateBoxMouseClick, null, canvasRotateBoxMouseMove, canvasRotateBoxMouseDown, null, null, null));
  //Following two settings should probably be defaults?
  canvas.mouse.moveUpdate = true; //Continual update of deltaX/Y
  defaultMouse = document.mouse = canvas.mouse;

  //Attach viewer object to canvas
  canvas.viewer = viewer;

  //Initial/default state
  var initial = {};
  initial.views = [];
  var view = {};
  view.min = [-1,-1,-1];
  view.max = [-1,-1,-1];
  initial.views.push(view);
  initial.properties = {};
  intitial.properties.resolution = [100,100];

  viewer.loadFile(JSON.stringify(initial));

  return viewer;
}

function canvasRotateBoxMouseClick(event, mouse) {
  mouse.element.viewer.rotation = '' + mouse.element.viewer.getRotationString();
  return false;
}

function canvasRotateBoxMouseDown(event, mouse) {
  return false;
}

var hideRotateBoxTimer;

function canvasRotateBoxMouseMove(event, mouse) {
  if (!mouse.element.viewer) return true;

  //Switch buttons for translate/rotate
  var button = mouse.button;

  //console.log(mouse.deltaX + "," + mouse.deltaY);
  switch (button)
  {
    case 0:
      mouse.element.viewer.rotateY(mouse.deltaX/5);
      mouse.element.viewer.rotateX(mouse.deltaY/5);
      break;
    case 1:
      mouse.element.viewer.rotateZ(Math.sqrt(mouse.deltaX*mouse.deltaX + mouse.deltaY*mouse.deltaY)/5);
      break;
  }

  mouse.element.viewer.draw();

  return false;
}

//This object encapsulates a vertex buffer and shader set
function RotateBoxRenderer(gl, colour) {
  this.gl = gl;
  if (colour)
    this.colour = colour;
  else
    this.colour = [0.5, 0.5, 0.5, 1.0];

  //Line renderer
  this.attribSizes = [3 * Float32Array.BYTES_PER_ELEMENT];

  this.elements = 0;
  this.elementSize = 0;
  for (var i=0; i<this.attribSizes.length; i++)
    this.elementSize += this.attribSizes[i];
}

RotateBoxRenderer.prototype.init = function() {
  //Compile the shaders
  this.program = new WebGLProgram(this.gl, "line-vs", "line-fs");
  if (this.program.errors) console.log(this.program.errors);
  //Setup attribs/uniforms (flag set to skip enabling attribs)
  this.program.setup(undefined, undefined, true);

  return true;
}

RotateBoxRenderer.prototype.updateBuffers = function(view) {
  //Create buffer if not yet allocated
  if (this.vertexBuffer == undefined) {
    //Init shaders etc...
    if (!this.init()) return;
    this.vertexBuffer = this.gl.createBuffer();
    this.indexBuffer = this.gl.createBuffer();
  }

  //Bind buffers
  this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexBuffer);
  this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, this.indexBuffer);

  this.box(view.min, view.max);
}

RotateBoxRenderer.prototype.box = function(min, max) {
  var zero = [min[0]+0.5*(max[0] - min[0]), min[1]+0.5*(max[1] - min[1]), min[2]+0.5*(max[2] - min[2])];
  var min10 = [min[0] + 0.45*(max[0] - min[0]), min[1]+0.45*(max[1] - min[1]), min[2]+0.45*(max[2] - min[2])];
  var max10 = [min[0] + 0.55*(max[0] - min[0]), min[1]+0.55*(max[1] - min[1]), min[2]+0.55*(max[2] - min[2])];
  var vertices = new Float32Array(
        [
          /* Bounding box */
          min[0], min[1], max[2],
          min[0], max[1], max[2],
          max[0], max[1], max[2],
          max[0], min[1], max[2],
          min[0], min[1], min[2],
          min[0], max[1], min[2],
          max[0], max[1], min[2],
          max[0], min[1], min[2],
          /* 10% box */
          min10[0], min10[1], max10[2],
          min10[0], max10[1], max10[2],
          max10[0], max10[1], max10[2],
          max10[0], min10[1], max10[2],
          min10[0], min10[1], min10[2],
          min10[0], max10[1], min10[2],
          max10[0], max10[1], min10[2],
          max10[0], min10[1], min10[2],
          /* Axis lines */
          min[0], zero[1], zero[2],
          max[0], zero[1], zero[2],
          zero[0], min[1], zero[2],
          zero[0], max[1], zero[2],
          zero[0], zero[1], min[2],
          zero[0], zero[1], max[2]
        ]);

  var indices = new Uint16Array(
        [
          /* Bounding box */
          0, 1, 1, 2, 2, 3, 3, 0,
          4, 5, 5, 6, 6, 7, 7, 4,
          0, 4, 3, 7, 1, 5, 2, 6,
          /* 10% box */
          8, 9, 9, 10, 10, 11, 11, 8,
          12, 13, 13, 14, 14, 15, 15, 12,
          8, 12, 11, 15, 9, 13, 10, 14,
          /* Axis lines */
          16, 17,
          18, 19,
          20, 21
        ]
     );
  this.gl.bufferData(this.gl.ARRAY_BUFFER, vertices, this.gl.STATIC_DRAW);
  this.gl.bufferData(this.gl.ELEMENT_ARRAY_BUFFER, indices, this.gl.STATIC_DRAW);
  this.elements = 24+24+6;
}

RotateBoxRenderer.prototype.draw = function(webgl) {
  if (!this.elements) return;

  if (this.program.attributes["aVertexPosition"] == undefined) return; //Require vertex buffer

  webgl.use(this.program);
  webgl.setMatrices();

  //Bind buffers
  this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexBuffer);
  this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, this.indexBuffer);

  //Enable attributes
  for (var key in this.program.attributes)
    this.gl.enableVertexAttribArray(this.program.attributes[key]);

 
  //Line box render
  this.gl.vertexAttribPointer(this.program.attributes["aVertexPosition"], 3, this.gl.FLOAT, false, 0, 0);
  //Bounding box
  this.gl.uniform4f(this.program.uniforms["uColour"], this.colour[0], this.colour[1], this.colour[2], this.colour[3]);
  this.gl.drawElements(this.gl.LINES, 24, this.gl.UNSIGNED_SHORT, 0);
  //10% box
  this.gl.drawElements(this.gl.LINES, 24, this.gl.UNSIGNED_SHORT, 24 * 2);
  //Axes (2 bytes per unsigned short)
  this.gl.uniform4f(this.program.uniforms["uColour"], 1.0, 0.0, 0.0, 1.0);
  this.gl.drawElements(this.gl.LINES, 2, this.gl.UNSIGNED_SHORT, (24+24) * 2);
  this.gl.uniform4f(this.program.uniforms["uColour"], 0.0, 1.0, 0.0, 1.0);
  this.gl.drawElements(this.gl.LINES, 2, this.gl.UNSIGNED_SHORT, (24+24+2) * 2);
  this.gl.uniform4f(this.program.uniforms["uColour"], 0.0, 0.0, 1.0, 1.0);
  this.gl.drawElements(this.gl.LINES, 2, this.gl.UNSIGNED_SHORT, (24+24+4) * 2);

  //Disable attribs
  for (var key in this.program.attributes)
    this.gl.disableVertexAttribArray(this.program.attributes[key]);

  this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);
  this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, null);
  this.gl.useProgram(null);
}

//This object holds the viewer details and calls the renderers
function RotateBoxViewer(canvas) {
  this.canvas = canvas;
  if (!canvas) {alert("Invalid Canvas"); return;}
  try {
    this.webgl = new WebGL(this.canvas, {antialias: true}); //, premultipliedAlpha: false});
    this.gl = this.webgl.gl;
  } catch(e) {
    //No WebGL
    console.log("No WebGL: " + e);
  }

  this.translate = [0,0,0];
  this.rotate = quat4.create();
  quat4.identity(this.rotate);
  this.fov = 45;
  this.focus = [0,0,0];
  this.centre = [0,0,0];
  this.near_clip = this.far_clip = 0.0;
  this.modelsize = 1;
  this.scale = [1, 1, 1];
  this.orientation = 1.0; //1.0 for RH, -1.0 for LH

  //Non-persistant settings
  this.mode = 'Rotate';
  if (!this.gl) return;

  //Create the renderers
  this.border = new RotateBoxRenderer(this.gl, [0.5,0.5,0.5,1]);

  this.gl.enable(this.gl.DEPTH_TEST);
  this.gl.depthFunc(this.gl.LEQUAL);
  //this.gl.depthMask(this.gl.FALSE);
  this.gl.enable(this.gl.BLEND);
  //this.gl.blendFunc(this.gl.SRC_ALPHA, this.gl.ONE_MINUS_SRC_ALPHA);
  //this.gl.blendFuncSeparate(this.gl.SRC_ALPHA, this.gl.ONE_MINUS_SRC_ALPHA, this.gl.ZERO, this.gl.ONE);
  this.gl.blendFuncSeparate(this.gl.SRC_ALPHA, this.gl.ONE_MINUS_SRC_ALPHA, this.gl.ONE, this.gl.ONE_MINUS_SRC_ALPHA);
}

RotateBoxViewer.prototype.exportView = function(nocam) {
  //Update camera settings of current view
  if (nocam)
    this.view = {};
  else {
    this.view.rotate = this.getRotation();
    this.view.focus = this.focus;
    this.view.translate = this.translate;
    this.view.scale = this.scale;
  }
  this.view.aperture = this.fov;
  this.view.near = this.near_clip;
  this.view.far = this.far_clip;
  this.view.border = this.showBorder ? 1 : 0;
  //this.view.background = this.background.toString();

  //Never export min/max
  var V = Object.assign(this.view);
  V.min = undefined;
  V.max = undefined;
  return [V];
}

RotateBoxViewer.prototype.loadFile = function(source) {
console.log(source);
  //Skip update to rotate/translate etc if in process of updating
  //if (document.mouse.isdown) return;
  if (source.length < 3) {
    console.log('Invalid source data, ignoring');
    console.log(source);
    console.log(RotateBoxViewer.prototype.loadFile.caller);
    return; //Invalid
  }

  //Parse data
  var src = {};
  try {
    src = JSON.parse(source);
  } catch(e) {
    console.log(source);
    console.log("Parse Error: " + e);
    return;
  }

  //Set active view (always first for now)
  this.view = this.vis.views[0];
  if (this.view) {
    this.fov = this.view.aperture || 45;
    this.near_clip = this.view.near || 0;
    this.far_clip = this.view.far || 0;
    this.orientation = this.view.orientation || 1;
  }

  if (this.vis.properties.resolution && this.vis.properties.resolution[0] && this.vis.properties.resolution[1]) {
    this.width = this.vis.properties.resolution[0];
    this.height = this.vis.properties.resolution[1];
  }
  this.updateDims(this.view);

  //Update display
  if (!this.gl) return;
  this.draw();
  this.clear();
}

RotateBoxViewer.prototype.clear = function() {
  if (!this.gl) return;
  this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
}

RotateBoxViewer.prototype.draw = function() {
  if (!this.canvas) return;

  //Get the dimensions from the current canvas
  if (this.width != this.canvas.offsetWidth || this.height != this.canvas.offsetHeight) {
    this.width = this.canvas.offsetWidth;
    this.height = this.canvas.offsetHeight;
    //Need to set this too for some reason
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    if (this.gl) {
      this.gl.viewportWidth = this.width;
      this.gl.viewportHeight = this.height;
      this.webgl.viewport = new Viewport(0, 0, this.width, this.height);
    }
  }
  if (!this.gl) return;

  this.gl.viewport(0, 0, this.gl.viewportWidth, this.gl.viewportHeight);
  //this.gl.clearColor(1, 1, 1, 0);
  this.gl.clearColor(0, 0, 0, 0);
  this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);

  this.webgl.view(this);

  //Render objects
  this.border.draw(this.webgl);

}

RotateBoxViewer.prototype.rotateX = function(deg) {
  this.rotation(deg, [1,0,0]);
}

RotateBoxViewer.prototype.rotateY = function(deg) {
  this.rotation(deg, [0,1,0]);
}

RotateBoxViewer.prototype.rotateZ = function(deg) {
  this.rotation(deg, [0,0,1]);
}

RotateBoxViewer.prototype.rotation = function(deg, axis) {
  //Quaterion rotate
  var arad = deg * Math.PI / 180.0;
  var rotation = quat4.fromAngleAxis(arad, axis);
  rotation = quat4.normalize(rotation);
  this.rotate = quat4.multiply(rotation, this.rotate);
}

RotateBoxViewer.prototype.getRotation = function() {
  return [this.rotate[0], this.rotate[1], this.rotate[2], this.rotate[3]];
}

RotateBoxViewer.prototype.getRotationString = function() {
  //Return current rotation quaternion as string
  var q = this.getRotation();
  return 'rotation ' + q[0] + ' ' + q[1] + ' ' + q[2] + ' ' + q[3];
}

RotateBoxViewer.prototype.reset = function() {
  if (this.gl) {
    this.updateDims(this.view);
    this.draw();
  }

  this.command('reset');
}

RotateBoxViewer.prototype.updateDims = function(view) {
  if (!view) return;

  //Check for valid dims
  for (var i=0; i<3; i++) {
    view.max[i] = 1.0;
    view.min[i] = -1.0;
  }

  this.dims = [view.max[0] - view.min[0], view.max[1] - view.min[1], view.max[2] - view.min[2]];
  this.modelsize = Math.sqrt(this.dims[0]*this.dims[0] + this.dims[1]*this.dims[1] + this.dims[2]*this.dims[2]);

  this.focus = [view.min[0] + 0.5*this.dims[0], view.min[1] + 0.5*this.dims[1], view.min[2] + 0.5*this.dims[2]];
  this.centre = [this.focus[0],this.focus[1],this.focus[2]];

  this.translate = [0,0,0];
  if (this.modelsize != oldsize) this.translate[2] = -this.modelsize*1.25;

  if (this.near_clip == 0.0) this.near_clip = this.modelsize / 10.0;   
  if (this.far_clip == 0.0) this.far_clip = this.modelsize * 10.0;

  quat4.identity(this.rotate);

  //console.log("DIMS: " + view.min[0] + " to " + view.max[0] + "," + view.min[1] + " to " + view.max[1] + "," + view.min[2] + " to " + view.max[2]);
  //console.log("New model size: " + this.modelsize + ", Focal point: " + this.focus[0] + "," + this.focus[1] + "," + this.focus[2]);
  //console.log("Translate: " + this.translate[0] + "," + this.translate[1] + "," + this.translate[2]);

  if (!this.gl) return;
 
  //Create the bounding box vertex buffer
  this.border.updateBuffers(this.view);
}
