$(document).ready(function() {
    $("#loadMore").on('click', function(){
        var _currentProducts=$(".product-box").length;
        var _limit=$(this).attr('data-limit');
        var _total=$(this).attr('data-total');
        //start Ajax
        $.ajax({
			url:'/load-more-data',
			data:{
                limit:_limit,
                offset:_currentProducts
            },
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
                $(".load-more-icon").addClass('fa-spin'); // animating the load icon
			},
			success:function(res){
                $("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
                $(".load-more-icon").removeClass('fa-spin');
                
                
                var _totalShowing=$(".product-box").length;
                if(_totalShowing==_total){
                    $("#loadMore").remove();
                }
            }
		});
        //end Ajax
    });
    //pShow seleced price for the size
    $(".choose-size").on('click', function(){
        var _price=$(this).attr('data-price');
        $(".product-price").text(_price);
        $(".choose-size").removeClass('active'); // remove active class from all sizes
        $(this).addClass('active'); // add active class to clicked size
    });
    //end product variation
    
    //Set default size and highlight it
    $(".choose-size:first").addClass('active').trigger('click');


    //add to card
    $(document).on('click',".add-to-cart", function(){
        var _vm=$(this);
        var _index=_vm.attr('data-index');
        var _qty=$(".product-qty-"+_index).val();
        var _productId=$(".product-id-"+_index).val();
        var _productImage=$(".product-image-"+_index).val()
        var _productTitle=$(".product-title-"+_index).val();
        var _productPrice=$(".product-price-"+_index).text();

        //ajax starts
        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':_productId,
                'image':_productImage,
                'qty':_qty,
                'title':_productTitle,
                'price':_productPrice

            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
            }
        });
        //end Ajax
    });
    //end

    //delete item from cart
    $(document).on('click','.delete-item',function(){
        var _pId=$(this).attr('data-item');
        var _vm=$(this);
        //ajax starts
        $.ajax({
            url:'/delete-from-cart',
            data:{
                'id':_pId
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
                $("#cartlist").html(res.data);
            }
        });
        //end Ajax
    });

	// Update item from cart
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
    });

    // Add wishlist
	$(document).on('click',".add-wishlist",function(){
		var _pid=$(this).attr('data-product');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:"/add-wishlist",
			data:{
				product:_pid
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					_vm.addClass('disabled').removeClass('add-wishlist');
				}
			}
		});
		// EndAjax
	});
    
});
//end Document.Ready

// Product Review Save
$("#addForm").submit(function(e){
	$.ajax({
		data:$(this).serialize(),
		method:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType:'json',
		success:function(res){
			if(res.bool==true){
				$(".ajaxRes").html('Data has been added.');
				$("#reset").trigger('click');
				// create data for review
				var _html='<blockquote class="blockquote text-right">';
				_html+='<small>'+res.data.review_text+'</small>';
				_html+='<footer class="blockquote-footer">'+res.data.user;
				_html+='<cite title="Source Title">';
				for(var i=1; i<=res.data.review_rating; i++){
					_html+='<i class="fa fa-star text-warning"></i>';
				}
				_html+='</cite>';
				_html+='</footer>';
				_html+='</blockquote>';
				_html+='</hr>';
                
                $(".no-data").hide();

				// Prepend Data
				$(".review-list").prepend(_html);

				// Hide Modal
				$("#productReview").modal('hide');

				// AVg Rating
				$(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))
		
			}
		}
	});
	e.preventDefault();
});
// End