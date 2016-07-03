$(document).ready(function(){
	$('.settings-nav ul li').click(function(){
		var _this=$(this);
		$('.settings-nav ul li').removeClass('selected');
		_this.addClass('selected');
		$('.profile-settings-wrapper').hide();$('.security-settings-wrapper').hide();$('.privacy-settings-wrapper').hide();$('.resume-settings-wrapper').hide();
		var _decision = _this.children().html();
		if(_decision=='Profile Settings'){
			$('.profile-settings-wrapper').show();
		}else if(_decision=='Security Settings'){
			$('.security-settings-wrapper').show();
		}else if(_decision=='Privacy Settings'){
			$('.privacy-settings-wrapper').show();
		}else if(_decision=='Skill Settings'){
			$('.resume-settings-wrapper').show();
		}
	});
});