from flask import Blueprint, render_template, request, redirect, url_for
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

items_bp = Blueprint('items', __name__)

@items_bp.route('/items')
def items():
    try:
        response = requests.get('https://api-ghost-dev.srv.volvo.com/api/ApplicationConfiguration/GetAllConfigurations', verify=False)
        if response.status_code == 200:
            items = response.json()
            #print(items)  # Print the fetched data to the console for debugging
        else:
            items = []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        items = []
    return render_template('items.html', items=items)

@items_bp.route('/items/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        Key = request.form['Key']
        Value = request.form['Value']
        System = request.form['System']
        # Here you would typically send a POST request to your API to create the new item
        # For example:
        response = requests.post('https://api-ghost-dev.srv.volvo.com/api/ApplicationConfiguration/SaveApplicationConfiguration', json={'Key': Key, 'Value': Value, 'System': System}, verify=False)
        # if response.status_code == 201:
        #     return redirect(url_for('items.items'))
        # else:
        #     # Handle error
        #     pass
        # For now, we'll just redirect back to the items page
        return redirect(url_for('items.items'))
    return render_template('create_item.html')

@items_bp.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if request.method == 'POST':
        Key = request.form['Key']
        Value = request.form['Value']
        System = request.form['System']
        # Here you would typically send a PUT request to your API to update the item
        # For example:
        response = requests.put(f'https://api-ghost-dev.srv.volvo.com/api/ApplicationConfiguration/UpdateApplicationConfiguration', json={'Id':item_id,'Key': Key, 'Value': Value, 'System': System}, verify=False)
        # if response.status_code == 200:
        #     return redirect(url_for('items.items'))
        # else:
        #     # Handle error
        #     pass
        # For now, we'll just redirect back to the items page
        return redirect(url_for('items.items'))
    else:
        # Fetch the item details to pre-fill the form
        # For example:
        # response = requests.get(f'https://api-ghost-dev.srv.volvo.com/api/ApplicationConfiguration/GetConfiguration/{item_id}', verify=False)
        # if response.status_code == 200:
        #     item = response.json()
        # else:
        #     item = None
        # For now, we'll use a placeholder item
        item = {'id': item_id, 'name': 'Sample Name', 'description': 'Sample Description'}
    return render_template('edit_item.html', item=item)

@items_bp.route('/items/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    # Here you would typically send a DELETE request to your API to delete the item
    # For example:
    response = requests.delete(f'https://api-ghost-dev.srv.volvo.com/api/ApplicationConfiguration/DeleteApplicationConfiguration?id={item_id}', verify=False)
    # if response.status_code == 204:
    #     return redirect(url_for('items.items'))
    # else:
    #     # Handle error
    #     pass
    # For now, we'll just redirect back to the items page
    return redirect(url_for('items.items'))