from flask import Flask,request,jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/database_name'
db = SQLAlchemy(app)
api = Api(app)

from server.APP.models import User, Organization, Donation, Story, Beneficiary, Inventory


# Define the resource classes
class UserResource(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                'User_ID': user.User_ID,
                'Username': user.Username,
                'Email': user.Email,
                'Role': user.Role
            }
            user_list.append(user_data)
        return user_list

class OrganizationResource(Resource):
    def get(self):
        organizations = Organization.query.all()
        org_list = []
        for org in organizations:
            org_data = {
                'Organization_ID': org.Organization_ID,
                'Name': org.Name,
                'Description': org.Description,
                'Contact_Information': org.Contact_Information,
                'Status': org.Status
            }
            org_list.append(org_data)
        return org_list

# Add more resource classes for Donation, Story, Beneficiary, and Inventory routes

class DonationResource(Resource):
    def get(self):
        # Retrieve donations for a specific organization
        organization_id = request.args.get('organization_id')
        donations = Donation.query.filter_by(Organization_ID=organization_id).all()
        donation_list = []
        for donation in donations:
            donation_data = {
                'Donation_ID': donation.Donation_ID,
                'Donor_User_ID': donation.Donor_User_ID,
                'Amount': donation.Amount,
                'Donation_Type': donation.Donation_Type,
                'Anonymous': donation.Anonymous,
                'Date': donation.Date
            }
            donation_list.append(donation_data)
        return donation_list

    def post(self):
        # Create a new donation
        donation_data = request.get_json()

        # Validate required fields
        required_fields = ['donor_user_id', 'organization_id', 'amount', 'donation_type', 'anonymous', 'date']
        for field in required_fields:
            if field not in donation_data or not donation_data[field]:
                return jsonify({'error': f"Missing or empty field: {field}"}), 400

        donor_user_id = donation_data['donor_user_id']
        organization_id = donation_data['organization_id']
        amount = donation_data['amount']
        donation_type = donation_data['donation_type']
        anonymous = donation_data['anonymous']
        date = donation_data['date']

        # Validate donor user
        donor_user = User.query.filter_by(id=donor_user_id, role='Donor').first()
        if not donor_user:
            return jsonify({'error': 'Invalid donor user ID'}), 400

        # Validate organization
        organization = Organization.query.get(organization_id)
        if not organization:
            return jsonify({'error': 'Invalid organization ID'}), 400

        # Perform data type validation if needed
        # ...

        # Save the donation to the database
        new_donation = Donation(
            donor_user_id=donor_user_id,
            organization_id=organization_id,
            amount=amount,
            donation_type=donation_type,
            anonymous=anonymous,
            date=date
        )
        db.session.add(new_donation)
        db.session.commit()


        return {'message': 'Donation created successfully'}, 201


class StoryResource(Resource):
    def post(self):
        # Create a new story
        data = request.get_json()

        # Validate required fields
        required_fields = ['organization_id', 'title', 'content', 'images', 'date_created']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f"Missing or empty field: {field}"}), 400

        organization_id = data['organization_id']
        title = data['title']
        content = data['content']
        images = data['images']
        date_created = data['date_created']

        # Validate organization
        organization = Organization.query.get(organization_id)
        if not organization:
            return jsonify({'error': 'Invalid organization ID'}), 400

        # Perform data type validation if needed
        # ...

        # Create new story
        new_story = Story(
            organization_id=organization_id,
            title=title,
            content=content,
            images=images,
            date_created=date_created
        )
        db.session.add(new_story)
        db.session.commit()

        return {'message': 'Story created successfully'}, 201


class BeneficiaryResource(Resource):
    def get(self):
        # Retrieve beneficiaries for a specific organization
        organization_id = request.args.get('organization_id')
        beneficiaries = Beneficiary.query.filter_by(Organization_ID=organization_id).all()
        beneficiary_list = []
        for beneficiary in beneficiaries:
            beneficiary_data = {
                'Beneficiary_ID': beneficiary.Beneficiary_ID,
                'Name': beneficiary.Name,
                'Description': beneficiary.Description,
                'Inventory_Received': beneficiary.Inventory_Received
            }
            beneficiary_list.append(beneficiary_data)
        return beneficiary_list

    def post(self):
        # Create a new beneficiary
        data = request.get_json()

        # Validate required fields
        required_fields = ['organization_id', 'name', 'description', 'inventory_received']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f"Missing or empty field: {field}"}), 400

        organization_id = data['organization_id']
        name = data['name']
        description = data['description']
        inventory_received = data['inventory_received']

        # Validate organization
        organization = Organization.query.get(organization_id)
        if not organization:
            return jsonify({'error': 'Invalid organization ID'}), 400

        # Perform data type validation if needed
        # ...

        # Save the beneficiary to the database
        new_beneficiary = Beneficiary(
            organization_id=organization_id,
            name=name,
            description=description,
            inventory_received=inventory_received
        )
        db.session.add(new_beneficiary)
        db.session.commit()

        return {'message': 'Beneficiary created successfully'}, 201




class InventoryResource(Resource):
    def get(self):
        # Retrieve inventory for a specific beneficiary
        beneficiary_id = request.args.get('beneficiary_id')
        inventory = Inventory.query.filter_by(Beneficiary_ID=beneficiary_id).all()
        inventory_list = []
        for item in inventory:
            item_data = {
                'Inventory_ID': item.Inventory_ID,
                'Beneficiary_ID': item.Beneficiary_ID,
                'Description': item.Description,
                'Quantity': item.Quantity,
                'Date_Received': item.Date_Received
            }
            inventory_list.append(item_data)
        return inventory_list

    def post(self):
        # Create a new inventory item
        data = request.get_json()

        # Validate required fields
        required_fields = ['beneficiary_id', 'description', 'quantity', 'date_received']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f"Missing or empty field: {field}"}), 400

        beneficiary_id = data['beneficiary_id']
        description = data['description']
        quantity = data['quantity']
        date_received = data['date_received']

        # Validate beneficiary
        beneficiary = Beneficiary.query.get(beneficiary_id)
        if not beneficiary:
            return jsonify({'error': 'Invalid beneficiary ID'}), 400

        # Perform data type validation if needed
        # ...

        # Save the inventory item to the database
        new_inventory_item = InventoryResource(
            beneficiary_id=beneficiary_id,
            description=description,
            quantity=quantity,
            date_received=date_received
        )
        db.session.add(new_inventory_item)
        db.session.commit()

        return {'message': 'Inventory item created successfully'}, 201