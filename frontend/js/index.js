var network;
var globalDATA;
var networkThem;
var networkCoref;

$(document).ready(function(){

    $.ajaxSetup({
        async:false
    }); 

  	manageOnOffSwitch();
  	manageSubmitButton();
  	manageNextPrevButtons();

});

function manageNextPrevButtons()
{

	$("#previous").click(function(){
		var currentGraph = parseInt($('#idGraph').attr("name"));

		if($( this ).css( "background-color" ) == "rgb(0, 0, 0)")
		{
			displayTree(globalDATA, currentGraph-1);
		}	
	});

	$("#next").click(function(){
		var currentGraph = parseInt($('#idGraph').attr("name"));
		if($( this ).css( "background-color" ) == "rgb(0, 0, 0)")
		{
			displayTree(globalDATA, currentGraph+1);
		}
	});
}


function manageSubmitButton()
{
	$("#submitButton").click(function(){

		$("#pillWrapper").show();
		$("#tabContent").show();

	  	var height = $( window ).height();
	  	height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 20;
	  	$("#graphContainer").height(height);
	  	$("#themContainer").height(height);
	  	$("#themProgContainer").height(height);
	  	$("#corefContainer").height(height);
	  	$("#argumentContainer").height(height);

	  	$("#header").hide()

	  	var text =  $('textarea#inputBox').val();
	  	var data = {"text": text};
        console.log(data)
	    $.post( "http://192.168.1.51:5000/getConll", data ,function( dataJSON ) {
		    displayTree(dataJSON, 0);
		    displayCorefs(dataJSON);
		    globalDATA = dataJSON;
		}, "json");

		$.post( "http://192.168.1.51:5000/getThematicity", function( dataJSON ) {
		    displayThem(dataJSON);
   		    displayArguments(dataJSON);

		}, "json");

		$.post( "http://192.168.1.51:5000/getThematicProgression", function( dataJSON ) {
		    displayThematicProgression(dataJSON);
		}, "json");

		$.post( "http://192.168.1.51:5000/getBlocks", function( dataJSON ) {
		    displayBlocks(dataJSON);
		}, "json");
		
		$("#myonoffswitch").prop("checked",false);
  	});
}

function getWav(text, i)
{
	console.log(i);

	fetch('http://localhost:5002/api/tts?text=' + encodeURIComponent(text), {cache: 'no-cache'}).then(function(res) {
			if (!res.ok) throw Error(res.statusText)
				return res.blob()
			}).then(function(blob) {
				let url = URL.createObjectURL(blob);
				$("#ttsContainer #block_"+i).append("<audio controls src="+url+"></audio>");
				$("#synth_"+i).hide();
			});

}

function displayBlocks(dataJSON)
{
	var obj = $.parseJSON(dataJSON);
	$("#ttsContainer").html();
	let idBlock = 1;
	for(var p = 0; p<obj["blocks"].length; p++)
	{
		var block = obj["blocks"][p];
		let blockStr = "";
		$("#ttsContainer").append("<div class='block' id='block_"+idBlock+"'></div>");
		$("#ttsContainer #block_"+idBlock).append("<b>Block "+idBlock+"</b>");
		$("#ttsContainer #block_"+idBlock).append("<ol></ol>");

		for(var q = 0; q<block.length; q++)
		{
			let text = block[q];
			blockStr += text + " ";
			$("#ttsContainer #block_"+idBlock+" ol").append("<li>"+text+"</li>");
		}
		
		$("#ttsContainer #block_"+idBlock).append("<button id=synth_"+idBlock+" class='synthesize btn btn-primary'>Synthesize</button>")
		idBlock++;

	}

	$(".synthesize").click(function()
	{
		let id = $(this).attr('id');
		id = id.replace("synth_","")
		let blockStr = $(this).parent().find("ol li").text();
		console.log(id, blockStr);
		getWav(blockStr, id);
		
	});
}

function displayArguments(dataJSON)
{
	var obj = $.parseJSON(dataJSON);
	var arguments = [];
	$("#argumentContainer").html();
	$("#argumentContainer").append("<ol>");

	for(var p = 0; p<obj["sentences"].length; p++)
	{
		var sentence = obj["sentences"][p]["text"];
		var them = obj["sentences"][p]["components"];
		var tokens = obj["sentences"][p]["tokens"];
		var pos = obj["sentences"][p]["pos"];

		var hasThem = false;
		var hasRhem = false;
		var startThem = -1;
		var endRhem = -1;
		var length = 0;
		var themNotPron = true;

		for(var n = 0; n < them[0].length; n++)
		{
			var from = them[0][n][0] - 1;
			var to = them[0][n][1] - 1;
			var label = them[0][n][2];
			var className;
			
			if(label[0] == "R")
			{
				hasRhem = true;
				endRhem = to;
			}
			else if(label[0] == "T")
			{
				var pronList = ["i","we","you"];
				hasThem = true;
				startThem = from;
				if(from == to)
				{
					posTheme = pos[from];
					lemmaTheme = tokens[from].toLowerCase();
					if(posTheme == "PRP" && ($.inArray(lemmaTheme, pronList) != -1))
					{
						themNotPron = false;
					}
				}
			}
			if(label[0] == "S")
			{
				if(from < startThem)
				{
					startThem = from;
				}
				if(to > endRhem)
				{
					endRhem = to;
				}
			}
			
			if(length < (endRhem - startThem))
			{
				length = endRhem - startThem;
			}
		}
		$("#argumentContainer").append("<ol>");

		console.log(sentence);
		console.log(hasThem && hasRhem && (length > (tokens.length - 3)) && themNotPron);
		if(hasThem && hasRhem && (length > (tokens.length - 3)) && themNotPron)
		{
			$("#argumentContainer").append("<li>"+sentence+"</li>");
		}
		$("#argumentContainer").append("</ol>");

	}
	
}

function displayThematicProgression(dataJSON)
{
	var nodes = [];
	var edges = [];

	var obj = $.parseJSON(dataJSON);
	var components = obj["components"];
	var hyper = obj["hypernode"];
	var distances = obj["distances"];


	var node = {};
    node.id = 0;
    node.label = "First Sentence";
    node.group = 0;
    node.title = hyper;
    nodes.push(node);

    var THEME_OFFSET = 100;
    var RHEME_OFFSET = 1000;

	for(var i = 0 ; i< components.length; i++)
	{
		var nodeTheme = {};
	    nodeTheme.id = i+THEME_OFFSET;
	    nodeTheme.label = "Theme";
	    nodeTheme.group = 1;
	    nodeTheme.title = components[i][0];
	    nodeTheme.shape="circle";
	    nodes.push(nodeTheme);

	    if( i < components.length-1)
	    {
		    var nodeRheme = {};
		    nodeRheme.id = i+RHEME_OFFSET;
		    nodeRheme.label = "Rheme";
		    nodeRheme.group = 2;
		    nodeRheme.title = components[i][1];
		    nodeRheme.shape="circle";
	    	nodes.push(nodeRheme);

		}
	}

	var THRESHOLD = 1;
	for(var j = 1; j< distances.length; j++)
	{
		
		if(distances[j][0] != -10 && distances[j][0] < THRESHOLD)
		{
			var edgeTheme = {};
			edgeTheme.from = j-1+THEME_OFFSET;
			edgeTheme.to = j+THEME_OFFSET
			if(distances[j][0] == "coref")
			{
				edgeTheme.label = "coref";
			}
			else{
				edgeTheme.label = String(distances[j][0].toFixed(2));
			}
			edgeTheme.font = {align: 'top'};
			edgeTheme.arrows = "from";
			edges.push(edgeTheme);
		}

		if(distances[j][1] != -10 && distances[j][1] < THRESHOLD)
		{
			var edgeRheme = {};
			edgeRheme.label = String(distances[j][1].toFixed(2));
			edgeRheme.from = j-1+RHEME_OFFSET;
			edgeRheme.to = j+THEME_OFFSET
			edgeRheme.font = {align: 'top'};
			edgeRheme.arrows = "from";
			edges.push(edgeRheme);
		}

		

		if(distances[j][2] != -10 && distances[j][2] < THRESHOLD)
		{
			var edgeHyper = {};
			edgeHyper.from = j+THEME_OFFSET
			edgeHyper.to = 0;
			edgeHyper.label = String(distances[j][2].toFixed(2));
			edgeHyper.font = {align: 'top'};
			edgeHyper.arrows = "to";
			edges.push(edgeHyper);
		}
		
	}

	var len = nodes.length;
	for(var i = 0 ; i< len; i++)
	{
		var id = nodes[i].id;
		var found = false;
		for(var j=0; j< edges.length;j++)
		{
			if(edges[j].from == id || edges[j].to == id)
			{
				found = true;
				break;
			}
		}
		if(!found)
		{
			nodes.splice(i,1);
			len = nodes.length;
			i--;
		}
	}


	var container = document.getElementById('themProgContainer');
    var data = {
        nodes: nodes, 
        edges: edges
    };
    var options = {

	};

    networkThem = new vis.Network(container, data, options);


  	$('#them a').on('click', function (e) {
	  e.preventDefault();
	  $(this).tab('show');
	  networkThem.fit();
	});


}


function manageOnOffSwitch()
{
	$("#myonoffswitch").click(function(){
  	$("#header").toggle();
  	if($(this).is(":checked"))
  	{
  		var height = $( window ).height();
	  	height = height - $("#header").height() - $("#pillWrapper").height() - $(".onoffswitch").height() - 50;
	  	$("#graphContainer").height(height);
	  	$("#themContainer").height(height);
	  	$("#themProgContainer").height(height);
	  	$("#corefContainer").height(height);
	  	$("#argumentContainer").height(height);
  	}
  	else
  	{
  		var height = $( window ).height();
  		height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 50;
  		$("#graphContainer").height(height);
  		$("#themContainer").height(height);
	  	$("#themProgContainer").height(height);
	  	$("#corefContainer").height(height);
	  	$("#argumentContainer").height(height);

  	}
  	//network.fit();
  });
}


function displayTree(dataJSON, i) 
{
	if($("#idGraph").length == 0)
	{
		$("#home").append("<input type='hidden' id='idGraph' name='"+i+"' />");
	}
	else
	{
		$("#idGraph").attr("name",i);
	}

	var obj = $.parseJSON(dataJSON);
	var tokens = obj["sentences"][i]["tokens"];

	var nodes = [];
	var edges = [];

	if(i - 1 >= 0)
	{
		$("#previous").css({"background-color":"black"});
	}
	else
	{
		$("#previous").css({"background-color":"grey"});
	}
	if(i+1 < obj["sentences"].length)
	{
		$("#next").css({"background-color":"black"});
	}
	else
	{
		$("#next").css({"background-color":"grey"});
	}

	/**
		Create nodes
	**/
	for (var i = 0; i < tokens.length; i++) {
	    var pieces = tokens[i].split("\t");
	    var node = {};
	    node.id = pieces[0];
	    node.label = pieces[1];
	    node.group = pieces[3][0];
	    node.title = pieces[3];
	    nodes.push(node);

	    if(node.id != pieces[5])
	    {
	    	var edge = {};
	    	edge.from = pieces[5];
	    	edge.to = node.id;
	    	edge.label = pieces[4];
	    	edge.arrows = "to";
	    	edges.push(edge);
	    }
	}	


	var container = document.getElementById('graphContainer');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        layout:{  
          "hierarchical":{  
            "nodeSpacing":150,
            "sortMethod" : 'directed'
          }
        }
    };
    network = new vis.Network(container, data, options);
    	
/*
    $("#synt").click(function(){
  		network.fit();
  	});
*/
  	$('#synt a').on('click', function (e) {
	  e.preventDefault();
	  $(this).tab('show');
 	  network.fit();

	});
}

function displayCorefs(dataJSON)
{
	var obj = $.parseJSON(dataJSON);
	var corefs = obj["corefs"];
	var nodes = [];
	var edges = [];
	/**
		Create nodes
	**/
	var idNode = 0;

	for (var i = 0; i < corefs.length; i++) 
	{
	    for(var j = 0; j < corefs[i].length; j++)
	    {
	    	var node = {};
		    node.id = idNode;
		    node.label = corefs[i][j];
		    node.group = j;
		    nodes.push(node);
		    idNode++;
	    }
	    idNode = idNode - corefs[i].length;
	    for(var j = 0; j < corefs[i].length - 1; j++)
	    {
	    	var edge = {};
	    	edge.from = idNode;
	    	edge.to = idNode + 1;
	    	edge.arrows = "to";
	    	edges.push(edge);
	    	idNode++;
	    }
	    idNode++;
	    
	}	
	var container = document.getElementById('corefContainer');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {

    };
    networkCoref = new vis.Network(container, data, options);
    	
  	$('#coref a').on('click', function (e) {
	  e.preventDefault();
	  $(this).tab('show');
 	  networkCoref.fit();

	});

}

function displayThem(dataJSON)
{
	var obj = $.parseJSON(dataJSON);
	$( "#themContainer" ).html("");

	for(var p = 0; p<obj["sentences"].length; p++)
	{
		var sentence = obj["sentences"][p]["text"];
		var them = obj["sentences"][p]["components"];
		var tokens = obj["sentences"][p]["tokens"];


		var dictHighlight = {};
		var currentSentSelector = "#sent_"+p;

		$( "#themContainer" ).append("<br/><br/><h4>Sentence Number "+(p+1)+"</h3><span id='sent_"+p+"'></span>");
		
		$(currentSentSelector).append("<span id='ann_in'><span class='proposition badge badge-pill badge-secondary'>"+sentence+"</span></span><br/>");

		for (var j = 0; j < them.length; j++) 
		{
			var sentenceArray = [];
			sentenceArray.push("<span id=ann_"+j+">");
			for(var c =0; c<tokens.length;c++)
			{
				sentenceArray.push(tokens[c]);
			}
			for(var n = 0; n < them[j].length; n++)
			{
				var from = them[j][n][0] - 1;
				var to = them[j][n][1] - 1;
				var label = them[j][n][2];
				var toAppend = "</span>";
				var toPrepend;
				//console.log(from, to, label);

				if(label[0] == "P")
				{
					toPrepend = "<span class='proposition badge badge-pill badge-secondary'>";
				}
				else if(label[0] == "R")
				{
					toPrepend = "<span class='rheme badge badge-pill badge-info'>";
				}
				else if(label[0] == "S")
				{
					toPrepend = "<span class='specifier badge badge-pill badge-success'>";
				}
				else
				{
					toPrepend = "<span class='theme badge badge-pill badge-primary'>";
				}

				sentenceArray[from+1] = toPrepend + sentenceArray[from+1];
				sentenceArray[to+1] = sentenceArray[to+1] + toAppend;

			
			}
			sentenceArray.push("</span><br/>");
			$(currentSentSelector).append(sentenceArray.join(" "))

		}
		$(currentSentSelector).append("<br/>");
	}
	$( "#themContainer" ).css({"overflow":"auto", "overflow-x":"none"});
	
}