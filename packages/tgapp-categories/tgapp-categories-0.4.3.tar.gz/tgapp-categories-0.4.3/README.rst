.. image:: https://travis-ci.org/axant/tgapp-categories.svg?branch=master
    :target: https://travis-ci.org/axant/tgapp-categories
.. image:: https://coveralls.io/repos/github/axant/tgapp-categories/badge.svg?branch=master
    :target: https://coveralls.io/github/axant/tgapp-categories?branch=master


About tgapp-categories
-------------------------
This pluggable allow you to manage (create, read, update, delete)
categories on a website.

Since version 0.4.0 categories can now be nested, categories have ``children``, ``siblings``, ``descendants``, ``parent`` properties.
If you installed a previous version using sqlalchemy then you need to run the migration with ``gearbox migrate-pluggable tgappcategories upgrade``

There are 2 images associated to every category

This pluggable application works with both sqlalchemy and ming

Installing
-------------------------------

tgapp-categories can be installed both from pypi or from github::

    pip install tgappcategories

should just work for most of the users

Plugging tgapp-categories
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with tgappcategories::

    plug(base_config, 'tgappcategories', 'categories')

You will be able to access the plugged application at
*http://localhost:8080/categories*.

Permissions
-----------
This pluggable creates a Permission named 'tgappcategories', that has to be assigned
to the categories management users group.
You can assign it with a migration or evolution, using alembic or tgext.evolve

example of an evolution with tgext.evolve and ming::

    class TgappCategories(Evolution):
    """Assigns the tgappcategories permission to Managers"""
    evolution_id = 'tgapp-categories'

    def evolve(self):
        log.info('TgappCategories migration running')

        g_managers = model.Group.query.find({'group_name': 'managers'}).one()

        p_tgappcategories = model.Permission.query.find(
            {'permission_name': 'tgappcategories'}).one()
        p_tgappcategories.groups = [g_managers]
        model.DBSession.flush_all()



Depot
-----
This pluggable **needs** depot in order to work
you can find depot at https://github.com/amol-/depot
after you inserted depot into your project configure a storage called ``category_images``
example::

    app_cfg['depot_backend_type'] = 'depot.io.memory.MemoryFileStorage'
    app_cfg['depot.category_images.backend'] = 'depot.io.memory.MemoryFileStorage'
    app_cfg['depot.category_images.prefix'] = 'category_images/'
    storages = {
        'category_images': 'category_image',
    }
    for storage in storages:
        prefix = 'depot.%s.' % storage
        print('Configuring Storage %s*' % prefix)
        DepotManager.configure(storage, app_cfg, prefix)
        DepotManager.alias(storages[storage], storage)

Available Hooks
---------------

tgapp-cateogries exposes some hooks to configure it's behavior, The hooks that can be used with TurboGears2 register_hook are:
    * **categories.after_update(category, kwargs) -> Runs after a category is updated.
