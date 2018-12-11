var data_pointobj=new Object;
var data_type_list = new Object;
var data_type = new Object;	


data_pointobj = {
	Operation_type:'save',
	model_select_uri:'', //请求url
	data_name:'',        //数据点名称
	show_name:'',        //数据点显示名称
	TLV_Type:'',         //TLV_Type
	operation_type:'',   //操作类型 只读或者读写
	data_type:'',        //数据类型
	datalen:'',          //数据长度
	max_value : '',      //数字类型数据最大值
	min_value : '',		 // 数字类型数据最小值
	step_by_step: '',    // 数字类型数据步进值
	value_unit: '',      //数字类型数据单位
	true_value_name: '', // bool型数据 true值名称
	true_value_show: '', // bool型数据 true值显示名称
	true_bool_value: '', // 值为true
	false_value_name: '',// bool型数据 true值名称
	false_value_show: '',// bool型数据 true值显示名称
	false_bool_value: '',// 值为false
	str_maxlen:'',       //字符串最大长度
}

data_type_list = {
	'number':{
		'Char(-2^7-1 ~ 2^7,1字节)':'Char',	
		'uChar(0 ~ 2^8,1字节)'	:'UChar',											
		'Short(-2^15-1 ~ 2^15,2字节)':'Short',
	    'uShort(0 ~ 2^16,2字节)' :'UShort',                                        				
	    'Int(-2^31-1~ 2^31,4字节)':'Int' ,                                       
	    'uInt(0 ~ 2^32,4字节)'  :'UInt'  ,                                       
		'Long Long(-2^63-1 ~ 2^63,8字节)':'Long Long',											
	    'uLong Long(0 ~ 2^64,8字节)':'ULong Long',                                          
		'Float(-3.40282^-38 ~ 3.40282^38,4字节)':'Float',											
		'Double(-1.79769^-308 ~ 1.79769^308,8字节)':'Double',
	},											
	'Bool(布尔,单字节)':'Bool',											
	'Enum(枚举,单字节)':'Enum',											
	'String(十六进制)':'HexStr',											
	'String(UTF-8编码)'	:'UTF8Str',									
}

data_type = {
	'number':[
			'Char',	
			'UChar',											
			'Short',
		    'UShort' ,                                        				
		    'Int',                                       
		    'UInt',                                       
			'Long Long',											
		    'ULong Long',                                          
			'Float',											
			'Double',	
	],								
	'Bool(布尔,单字节)':'Bool',											
	'Enum(枚举,单字节)':'Enum',											
	'String':['HexStr','UTF8Str'],									
}

function is_chinese(str) {
		var reg = /^[\u4E00-\u9FA5]+$/; //中文正则 u4E00-u9FA5 是指在Unicode字符集里中文的开始字符与结束字符
		return reg.test(str)
}
function thefirstis_num(str) {
		var reg = /^[0-9]/; //
		return reg.test(str)
}
function alert_cancel(str){
	var on=confirm(str);
	if (on==true)
		return true
	else
		return false
}
//数据类型解码
function myPointDataType_Decode(tlvtype){
	var type = new String;
	Reflect.ownKeys(data_type_list).forEach(function(key){
		if (key == 'number')
		{
			Reflect.ownKeys(data_type_list[key]).forEach(function(key1){
				
				if (data_type_list[key][key1] == tlvtype)
				{
					type = key1;
				}
			});
		}
		else
		{
			if (data_type_list[key] == tlvtype)
			{
				type = key;
			}
		}
	});
	return type;
}

//获取数据点名称，用于上下行数据选择
function Get_DataPointName(model_name){
	var point_exsisted = new Array;//保存已经创建的数据点
	var model_nameobj = document.getElementById(model_name);//返回当前元素对象
	var point = model_nameobj.getElementsByClassName("point");
	var updata_selectpoint = document.getElementById("select_point");
	for(var i=0; i<point.length;i++)
	{
		point_exsisted[i] = document.getElementsByClassName('showname')[i].id;
		var optionsobj = document.createElement('option');
		optionsobj.innerHTML = point_exsisted[i];
		updata_selectpoint.appendChild(optionsobj);
	}
	return 	point_exsisted;
}

//获取已经存在的数据点数据，用于判断是否已经存在
function Get_DataPointattr(model_name,PointName,showname,tlvtype){
	var myPointNameArray = new Array;
	var tlvtypeArray =  new Array;
	var shownameArray = new Array;
	var model_nameobj = document.getElementById(model_name);//返回当前元素对象
	var point = model_nameobj.getElementsByClassName("point");


	for(var i=0; i<point.length;i++)
	{
		myPointNameArray[i] = document.getElementsByClassName('col-xs-3 col-sm-3 pointname')[i].id;
		tlvtypeArray[i]     = document.getElementsByClassName('col-xs-3 col-sm-3 tlvtype')[i].id;
		shownameArray[i]    = document.getElementsByClassName('showname')[i].id;
	}
	if (myPointNameArray.includes(PointName))
	{
		return 'PointName';
	}
	if (shownameArray.includes(showname))
	{
		return 'showname';
	}
	if (tlvtypeArray.includes(tlvtype))
	{
		return 'tlvtype';
	}
	return 'pass';
}

//添加警告框
function addmyalert(str,classname){
	var modal_position = document.getElementsByClassName(classname)[0];
	modal_position.setAttribute('data-toggle','popover');
	modal_position.setAttribute('data-content',str);
	modal_position.setAttribute('data-placement','top');
}


//修改数据点时，获取该数据点的数据放着模态框，并且可修改
function updatemodal(point_id){
	var dataarray = new	 Array;
	var decodetype = "";
	var clsobj = document.getElementById(point_id);
	var showname  = clsobj.getElementsByClassName('showname')[0];
	var pointname = clsobj.getElementsByClassName('col-xs-3  col-sm-3 pointname')[0];
	var tlvtype   = clsobj.getElementsByClassName('col-xs-3  col-sm-3 tlvtype')[0];
	var operation = clsobj.getElementsByClassName('col-xs-3  col-sm-3 operation')[0];
	var datatype  = clsobj.getElementsByClassName('col-xs-3  col-sm-3 datatype')[0];

	dataarray=[showname,pointname,tlvtype,operation,datatype];

	if (data_type['number'].includes(datatype.id))
	{
		var minvalue = clsobj.getElementsByClassName('col-xs-3  col-sm-3 minvalue')[0];
		var maxvalue = clsobj.getElementsByClassName('col-xs-3  col-sm-3 maxvalue')[0];
		var stepbystep = clsobj.getElementsByClassName('col-xs-3  col-sm-3 stepbystep')[0];
		var valueunit = clsobj.getElementsByClassName('col-xs-3  col-sm-3 valueunit')[0];

		dataarray.push(minvalue,maxvalue,stepbystep,valueunit);

		$('#exampleModal2').modal('show');

		$('#exampleModal2 #template_1').attr('style', "display:block");
        $('#exampleModal2 #template_2').attr('style', "display:none");
        $('#exampleModal2 #template_3').attr('style', "display:none");
         $("#exampleModal2 #DataType2").attr('name','number');

		$('.modal2showname').val(dataarray[0].id);
        $('.modal2pointname').val(dataarray[1].id);
        $('.model2tlvtype').val(dataarray[2].id);
        $('#exampleModal2 #Opteron_type').val(dataarray[3].id);

        decodetype= myPointDataType_Decode(dataarray[4].id);
        $('#exampleModal2 #DataType2').val(decodetype);

        $('#exampleModal2 #int_min_value').val(dataarray[5].id);
        $('#exampleModal2 #int_max_value').val(dataarray[6].id);
        $('#exampleModal2 #step_value').val(dataarray[7].id);
        $('#exampleModal2 #unit').val(dataarray[8].id);
	}
	else if (datatype.id == data_type['Bool(布尔,单字节)'])
	{
		var truevalue = clsobj.getElementsByClassName('col-xs-3  col-sm-3 truevalue')[0];
		var falsevalue = clsobj.getElementsByClassName('col-xs-3  col-sm-3 falsevalue')[0];

		
		dataarray.push(truevalue,falsevalue);

		$('#exampleModal2').modal('show');
        $('#exampleModal2 #template_1').attr('style', "display:none");
        $('#exampleModal2 #template_2').attr('style', "display:none");
        $('#exampleModal2 #template_3').attr('style', "display:block");
        $("#exampleModal2 #DataType2").attr('name','bool');		

		$('.modal2showname').val(dataarray[0].id);
        $('.modal2pointname').val(dataarray[1].id);
        $('.model2tlvtype').val(dataarray[2].id);
        $('#exampleModal2 #Opteron_type').val(dataarray[3].id);

        decodetype=myPointDataType_Decode(dataarray[4].id);
        $('#exampleModal2 #DataType2').val(decodetype);

        $('#exampleModal2 #true_name').val(dataarray[5].getAttribute('data-truevaluename'));
        $('#exampleModal2 #true_show_name').val(dataarray[5].getAttribute('data-trueshowname'));
        $('#exampleModal2 #false_name').val(dataarray[6].getAttribute('data-falsevaluename'));
        $('#exampleModal2 #false_show_name').val(dataarray[6].getAttribute('data-falseshowname'));

	}
	else if (data_type['String'].includes(datatype.id))
	{
		var strmaxlen = clsobj.getElementsByClassName('col-xs-3  col-sm-3 strmaxlen')[0];

		dataarray.push(strmaxlen);

		$('#exampleModal2').modal('show');
        $('#exampleModal2 #template_1').attr('style', "display:none");
        $('#exampleModal2 #template_2').attr('style', "display:block");
        $('#exampleModal2 #template_3').attr('style', "display:none");
        $("#exampleModal2 #DataType2").attr('name','str');		

		$('.modal2showname').val(dataarray[0].id);
        $('.modal2pointname').val(dataarray[1].id);
        $('.model2tlvtype').val(dataarray[2].id);
        $('#exampleModal2 #Opteron_type').val(dataarray[3].id);

        decodetype = myPointDataType_Decode(dataarray[4].id);
        $('#exampleModal2 #DataType2').val(decodetype);
        $('#exampleModal2 #str_maxlen').val(dataarray[5].id);
	}
	else
	{
			//枚举
	}	
}

//在上下行数据中，增加数据点
/*<div class="col-sm-3 col-sm-offset-1 "> 
    <label  style="font-size:16px;padding:5px;">数据点</label>
</div>
<div class="col-sm-3 col-xs-7 updataselect_point">
	<select class="form-control" id="select_point" >
		{% if Pointlist %}
			{% for point in Pointlist %}
				<option>{{point.show_name}}</option>
			{% endfor %}
		{% endif %}
	</select>
</div>
<div class="col-sm-3 col-xs-2 add_point_button">
	<div class="row">
		<button class="col-sm-3 col-xs-5 add addpoint_button" id="addpoint"><span class="glyphicon glyphicon-plus-sign"></span></button>
		<button class="col-sm-3 col-xs-5 add addpoint_button" id="delpoint"><span class="glyphicon glyphicon-minus-sign"></span></button>
	</div>		
</div>*/
function addpointbutton(model_name)
{
	var datapoint1=document.getElementsByClassName('row adddatapoint')[0];

	var cls1 = document.createElement('div');
	cls1.setAttribute('class',"col-sm-3 col-sm-offset-1");
	var label1 = document.createElement('label');
	label1.setAttribute('style',"font-size:16px;padding:5px;");
	label1.innerHTML = '数据点';
	cls1.appendChild(label1);

	var cls2 = document.createElement('div');
	cls2.setAttribute('class','col-sm-3 col-xs-7 updataselect_point');
	var	select1 = document.createElement('select');
	select1.setAttribute('class','form-control');
	select1.setAttribute('id','select_point');
	var pointarray=Get_DataPointName(model_name);
	console.log(pointarray);
	for(var i=0;i<pointarray.length;i++)
	{
		var option = new Array;
		option[i] = document.createElement('option');
		option[i].innerHTML = pointarray[i];
		select1.appendChild(option[i]);
	}
	cls2.appendChild(select1);

	var btndiv = document.createElement('div');
	btndiv.setAttribute('class','col-sm-3 col-xs-2 add_point_button');
	var ndiv   = document.createElement('div');
	ndiv.setAttribute('class','row');

	var addbtn = document.createElement('button');
	addbtn.setAttribute('class','col-sm-3 col-xs-5 add addpoint_button');
	addbtn.setAttribute('id','addpoint');
	addbtn.innerHTML = '<span class="glyphicon glyphicon-plus-sign"></span>';
	//var span1 = document.createElement('span');
	//span1.setAttribute('class','glyphicon glyphicon-plus-sign');

	var delbtn = document.createElement('button');
	delbtn.setAttribute('class','col-sm-3 col-xs-5 add addpoint_button');
	delbtn.setAttribute('id','delpoint');
	delbtn.innerHTML = '<span class="glyphicon glyphicon-minus-sign"></span>';

	btndiv.appendChild(ndiv);
	ndiv.appendChild(addbtn);
	ndiv.appendChild(delbtn);

	datapoint1.appendChild(cls1);
	datapoint1.appendChild(cls2);
	datapoint1.appendChild(btndiv);
}

function cloneaddpoint(){
	var datapoint = document.getElementsByClassName('row adddatapoint')[0];
	var clone1=document.getElementsByClassName('col-sm-3 col-sm-offset-1 datapoint')[0].cloneNode(true);
	var clone2=document.getElementsByClassName('col-sm-4 col-xs-7 updataselect_point')[0].cloneNode(true);
	var clone3 =document.getElementsByClassName(' col-sm-4 col-xs-3 add_point_button ')[0].cloneNode(true);
	datapoint.appendChild(clone1);
	datapoint.appendChild(clone2);
	datapoint.appendChild(clone3);
}

