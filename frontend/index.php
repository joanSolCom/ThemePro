<?php require "header.php" ?>

  	  <div id="textAreaWrapper">
	  	  <div>
		  	<textarea id="inputBox" class="md-textarea" placeholder="Write something here..."></textarea>
		  </div>
		  <div id= "wrapperButtons">
			  <button id="submitButton" class="btn btn-sample">Submit</button>
	      </div>
      </div>
    </div>
  	<div id="pillWrapper">
	  	<ul class="nav nav-pills btn-group">
		
		  <li id="synt" class="nav-item pill-1">
		  		<a class="btn btn-large btn-sample active" data-toggle="pill" href="#home">Syntactic Tree</a>
		  </li>
		  
		  <li class="nav-item pill-2">
		  		<a class="btn btn-large btn-sample" data-toggle="pill" href="#menu1">Thematicity</a>
		  </li>

		  <!--
		  <li id="them" class="nav-item pill-3">
		  		<a class="btn btn-large btn-sample" data-toggle="pill" href="#menu2">Thematic Progression</a>
		  </li>
			-->
		  <li id="coref" class="nav-item pill-4">
		  		<a class="btn btn-large btn-sample" data-toggle="pill" href="#menu3">Coref Chains</a>
		  </li>
		  <li id="tts" class="nav-item pill-5">
		  		<a class="btn btn-large btn-sample" data-toggle="pill" href="#menu4">ThemePro TTS</a>
		  </li>
	
		</ul>
	</div>

	<div id="tabContent" class="tab-content">
	  <div class="tab-pane container active" id="home">
	  		<div id="graphContainer" class="result">
	  			

	  		</div>
	  		<div id="pageButtons">
				<button id="previous" class="round">&#8249;</a>
				<button id="next" class="round">&#8250;</a>	  		
	  		</div>
	  </div>
	  <div class="tab-pane container" id="menu1">
		  	<div id="themContainer" class="result">
		  	</div>
	  </div>

	  <!--
	  <div class="tab-pane container" id="menu2">
		  	<div id="themProgContainer" class="result">
		  	</div>
	  </div>
	  -->

	  <div class="tab-pane container" id="menu3">
		  	<div id="corefContainer" class="result">
		  	</div>
	  </div>
	  
	  <div class="tab-pane container" id="menu4">
		  	<div id="ttsContainer" class="result">
		  	</div>
	  </div>
	  
	</div>



<?php require "footer.php" ?>