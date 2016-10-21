from django.shortcuts import render, redirect, HttpResponse
from .models import User, Wishlist, Item
from django.contrib import messages

def index(request):
	return render(request, 'pythonbelt/main.html')

def process(request):
	if request.method == 'POST':
		kwargs = {
			'name': request.POST['name'],
			'username': request.POST['username'],
			'password': request.POST['password'],
			'confirm_pw': request.POST['confirm_pw'],
			'date_hired': request.POST['date_hired']
		}

		user = User.objects.register(**kwargs)

		if user[0] == False:
			for error in user[1]:
				messages.error(request, error)
			return redirect('/')
		elif user[0] == True:
			request.session['user_id'] = user[1].id
			request.session["name"] = user[1].name
			return redirect('/dashboard')
	else:
		return redirect('/')


def login(request):
	if request.method == 'POST':
		kwargs = {
			'username': request.POST['username'],
			'password': request.POST['password'].encode()
		}	
		user = User.objects.login(**kwargs)
		
		if user[0] == False:
			messages.error(request,user[1])
			return redirect('/')
		elif user[0] == True:
			request.session['user_id'] = user[1].id
			request.session["name"] = user[1].name
			return redirect('/dashboard')
		return HttpResponse('Done running')
	else:
		return redirect('/')

def dashboard(request):
	context = {
		'items': Item.objects.all(),
		'users': User.objects.all(),
		'wishlist': Wishlist.objects.all()
	}
	return render(request, 'pythonbelt/dashboard.html', context)


def additem(request):
	return redirect('/wish_items/create')

def createItem(request):
	return render(request, 'pythonbelt/createItem.html')

def addNew(request):
	if request.method == 'POST':
		items = {
			'item_name': request.POST['item_name'],
			'user_id': request.session['user_id']
		}
		item = Item.objects.add(**items)

		if item[0] == False:
			messages.error(request, item[1])
			return redirect('/createItem')
		elif item[0] == True:
			request.session['item_id'] = item[1].id
			items['item_id']= request.session['item_id']
			wishlist = Wishlist.objects.newItem(**items)
			print wishlist
			return redirect('/dashboard')
		else:
			return redirect('/dashboard')	
	return redirect('/dashboard')

def item(request, id):
	# request.session['id'] = id
	# request.session['id_name'] = Item.objects.get(id=request.session['id']).item_name
	try: 
		item = Item.objects.get(id=id)
		
	except:
		return redirect('/books')
	context = {
		'item': item,
		'user': User.objects.all()
	}
	return render(request, 'pythonbelt/item.html', context)

def remove(request, id):
	if request.method == 'POST':
		request.session['id'] = id
		request.session['item_name'] = Item.objects.get(id=request.session['id']).item_name	
		Item.objects.get(id=request.session['id']).delete()
		request.session.clear()
	return redirect('/dashboard')

def delete(request):
	Item.objects.get(item_id=request.session['id']).delete()
	request.session.clear()
	return redirect('/dashboard')

def logout(request):
	request.session.clear()
	return redirect('/')