from django.shortcuts import render, redirect
from .models import AlphaGroup, Category, Voucher
from django.db.models import Q

# ALPHA GROUP LIST
def alpha_group_list(request):
    data = AlphaGroup.objects.all()
    categories = Category.objects.all()

    # 🔍 Filter by display name
    query = request.GET.get('q')
    if query:
        data = data.filter(display_name__icontains=query)

    # 🔍 Filter by category
    category = request.GET.get('category')
    if category:
        data = data.filter(category__id=category)

    return render(request, "alphagroup.html", {
        "data": data,
        "categories": categories
    })


# ADD GROUP
def add_group(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        display_name = request.POST.get("display_name")
        category_id = request.POST.get("category")

        category = Category.objects.get(id=category_id)

        AlphaGroup.objects.create(
            name=name,
            display_name=display_name,
            category=category
        )

        return redirect('alphagroup')

    return render(request, "add.html", {
        "categories": categories
    })


# EDIT GROUP
def edit_group(request, id):
    group = AlphaGroup.objects.get(id=id)
    categories = Category.objects.all()

    if request.method == "POST":
        group.name = request.POST.get("name")
        group.display_name = request.POST.get("display_name")
        group.category = Category.objects.get(id=request.POST.get("category"))
        group.save()

        return redirect('alphagroup')

    return render(request, "edit.html", {
        "group": group,
        "categories": categories
    })


# INACTIVE GROUP
def toggle_group_status(request, id):
    group = AlphaGroup.objects.get(id=id)

    group.is_active = not group.is_active   # 🔥 toggle
    group.save()

    return redirect('alphagroup')

# VOUCHER PAGE
def voucher(request):
    groups = AlphaGroup.objects.all()

    edit_id = request.GET.get("edit")
    edit_data = None

    if edit_id:
        edit_data = Voucher.objects.get(id=edit_id)

    if request.method == "POST":
        voucher_id = request.POST.get("voucher_id")

        voucher_no = request.POST.get("voucher_no")
        voucher_date = request.POST.get("voucher_date")
        remarks = request.POST.get("remarks")

        a_values = request.POST.getlist("amount_a[]")
        b_values = request.POST.getlist("amount_b[]")

        total_a = sum(float(a) for a in a_values if a)
        total_b = sum(float(b) for b in b_values if b)

        # 🔥 UPDATE
        if voucher_id:
            v = Voucher.objects.get(id=voucher_id)
            v.voucher_no = voucher_no
            v.voucher_date = voucher_date
            v.remarks = remarks
            v.total_a = total_a
            v.total_b = total_b
            v.save()
        else:
            # 🔥 CREATE
            Voucher.objects.create(
                voucher_no=voucher_no,
                voucher_date=voucher_date,
                remarks=remarks,
                total_a=total_a,
                total_b=total_b
            )

        return redirect("/voucher/")

    vouchers = Voucher.objects.filter(is_deleted=False)

    return render(request, "voucher.html", {
        "groups": groups,
        "vouchers": vouchers,
        "edit_data": edit_data
    })
# MARK DELETED (Soft Delete)
def mark_deleted(request, id):
    Voucher.objects.filter(id=id).update(is_deleted=True)
    return redirect('voucher')


# DELETE VOUCHER (Permanent)
def delete_voucher(request, id):
    Voucher.objects.filter(id=id).delete()
    return redirect('voucher')


# EDIT VOUCHER
def edit_voucher(request, id):
    voucher = Voucher.objects.get(id=id)
    categories = Category.objects.all()  # ✅ for base.html

    if request.method == "POST":
        voucher.voucher_no = request.POST.get("voucher_no")
        voucher.voucher_date = request.POST.get("voucher_date")
        voucher.remarks = request.POST.get("remarks")
        voucher.save()

        return redirect('voucher')

    return render(request, "edit_voucher.html", {
        "voucher": voucher,
        "categories": categories
    })

def voucher_popup(request):
    if request.method == "POST":
        voucher_no = request.POST.get("voucher_no")
        voucher_date = request.POST.get("voucher_date")
        remarks = request.POST.get("remarks")

        a_values = request.POST.getlist("amount_a[]")
        b_values = request.POST.getlist("amount_b[]")

        total_a = sum(float(a) for a in a_values if a)
        total_b = sum(float(b) for b in b_values if b)

        Voucher.objects.create(
            voucher_no=voucher_no,
            voucher_date=voucher_date,
            remarks=remarks,
            total_a=total_a,
            total_b=total_b
        )

        return redirect('alphagroup')

    return render(request, "voucher_popup.html")

def voucher_list(request):
    vouchers = Voucher.objects.filter(is_deleted=False)
    return render(request, "voucher_list.html", {
        "vouchers": vouchers
    })