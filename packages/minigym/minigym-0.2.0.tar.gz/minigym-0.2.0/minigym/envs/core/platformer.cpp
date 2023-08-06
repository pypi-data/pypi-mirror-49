#include <Python.h>
#include <structmember.h>
#include <Box2D/Box2D.h>

struct RenderFrame {
    b2Vec2 pos;
    float state;
    int progress;
};

struct Scene {
    PyObject_HEAD
    b2World * world;
    b2Body * character;

    RenderFrame render_frame[10];

    int frames;

    bool in_air;
    bool double_jump;
    bool moved_right;
    int progress;
};

PyTypeObject * Scene_type;

inline b2Body * static_box(b2World * world, float x, float y, float w, float h) {
    b2BodyDef body_def;
    body_def.position.Set(x, y);
    b2Body * body = world->CreateBody(&body_def);
    b2PolygonShape box;
    box.SetAsBox(w, h);
    b2FixtureDef fixture_def;
    fixture_def.shape = &box;
    fixture_def.density = 0.0f;
    fixture_def.friction = 0.0f;
    body->CreateFixture(&fixture_def);
    return body;
}

Scene * platformer_meth_scene(PyObject * self) {
    Scene * scene = PyObject_New(Scene, Scene_type);

    scene->frames = 0;
    scene->progress = 0;
    scene->in_air = false;
    scene->double_jump = true;
    scene->moved_right = true;

    scene->world = new b2World({0.0f, -10.0f});

    static_box(scene->world, 0.0f, -2.5f, 4.0f, 0.5f);
    static_box(scene->world, 2.5f, 0.5f, 1.5f, 0.5f);

    b2BodyDef character_def;
    character_def.type = b2_dynamicBody;
    character_def.position.Set(0.0f, -1.3f);
    scene->character = scene->world->CreateBody(&character_def);

    b2PolygonShape character_poly;
    character_poly.SetAsBox(0.3f, 0.4f);
    character_poly.m_radius = 0.1f;

    b2FixtureDef fixture_def;
    fixture_def.shape = &character_poly;
    fixture_def.density = 1.0f;
    fixture_def.friction = 0.0f;

    scene->character->CreateFixture(&fixture_def);
    scene->character->SetFixedRotation(true);

    return scene;
}

PyObject * Scene_meth_step(Scene * self, PyObject * args) {
    int step;

    if (!PyArg_ParseTuple(args, "i", &step)) {
        return NULL;
    }

    float reward = 0.0f;

    for (int frame = 0; frame < 10; ++frame) {
        b2Vec2 velocity = self->character->GetLinearVelocity();

        if (step == 1 || step == 4) {
            velocity.x = -4.0f;
        }
        if (step == 2 || step == 5) {
            velocity.x = 4.0f;
        }

        if (frame == 0 && step == 3) {
            if (!self->in_air || self->double_jump) {
                if (self->in_air) {
                    self->double_jump = false;
                }
                velocity.y = 8.0f;
            }
        }

        velocity.x *= 0.8f;
        self->character->SetLinearVelocity(velocity);

        self->world->Step(1.0f / 60.0f, 6, 2);

        self->in_air = true;
        for (b2Contact * c = self->world->GetContactList(); c; c = c->GetNext()) {
            if (c->GetFixtureA() == self->character->GetFixtureList() || c->GetFixtureB() == self->character->GetFixtureList()) {
                b2Manifold * m = c->GetManifold();
                b2WorldManifold w;
                c->GetWorldManifold(&w);
                if ((w.normal - b2Vec2(0.0f, 1.0f)).Length() < 1e-3) {
                    self->in_air = false;
                    self->double_jump = true;
                }
            }
        }

        float character_state = 0.0f;
        if (self->character->GetLinearVelocity().x > 0.1f) {
            self->moved_right = true;
        } else if (self->character->GetLinearVelocity().x < -0.1f) {
            self->moved_right = false;
        }

        if (self->in_air) {
            character_state = self->moved_right ? 6.0f : 7.0f;
        } else {
            if (self->character->GetLinearVelocity().x > 0.1f) {
                character_state = self->frames % 16 < 8 ? 2.0f : 3.0f;
            } else if (self->character->GetLinearVelocity().x < -0.1f) {
                character_state = self->frames % 16 < 8 ? 4.0f : 5.0f;
            } else {
                character_state = self->moved_right ? 0.0f : 1.0f;
            }
        }
        if (self->progress == 0 && (self->character->GetPosition() - b2Vec2(-3.5f, -1.5f)).Length() < 0.75f) {
            self->progress = 1;
            reward += 1.0f;
        }
        if (self->progress == 1 && (self->character->GetPosition() - b2Vec2(3.5f, 1.5f)).Length() < 0.1f) {
            self->progress = 2;
            reward += 1.0f;
        }

        self->render_frame[frame] = {self->character->GetPosition(), character_state, self->progress};

        self->frames += 1;
    }

    b2Vec2 position = self->character->GetPosition();
    PyObject * done = Py_False;

    if (position.y < -3.0f) {
        done = Py_True;
        reward -= 1.0f;
    }

    if (self->progress == 2 || self->frames >= 400) {
        done = Py_True;
    };

    reward -= 0.001f;

    return Py_BuildValue("(ff)fO{}", position.x, position.y, reward, done);
}

PyObject * Scene_meth_frames(Scene * self) {
    PyObject * res = PyList_New(10);
    for (int i = 0; i < 10; ++i) {
        const RenderFrame f = self->render_frame[i];
        PyList_SET_ITEM(res, i, Py_BuildValue("(fff)i", f.pos.x, f.pos.y + 0.2f, f.state, f.progress));
    }
    return res;
}

void Scene_dealloc(Scene * self) {
    delete self->world;
    Py_TYPE(self)->tp_free(self);
}

PyMethodDef Scene_methods[] = {
    {"step", (PyCFunction)Scene_meth_step, METH_VARARGS, NULL},
    {"frames", (PyCFunction)Scene_meth_frames, METH_NOARGS, NULL},
    {},
};

PyMemberDef Scene_members[] = {
    {"progress", T_INT, offsetof(Scene, progress), READONLY, NULL},
    {},
};

PyType_Slot Scene_slots[] = {
    {Py_tp_methods, Scene_methods},
    {Py_tp_members, Scene_members},
    {Py_tp_dealloc, Scene_dealloc},
    {},
};

PyType_Spec Scene_spec = {"platformer.Scene", sizeof(Scene), 0, Py_TPFLAGS_DEFAULT, Scene_slots};

PyMethodDef module_methods[] = {
    {"scene", (PyCFunction)platformer_meth_scene, METH_VARARGS, NULL},
    {},
};

PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "platformer", NULL, -1, module_methods};

extern "C" PyObject * PyInit_platformer() {
    PyObject * module = PyModule_Create(&module_def);
    Scene_type = (PyTypeObject *)PyType_FromSpec(&Scene_spec);
    PyModule_AddObject(module, "Scene", (PyObject *)Scene_type);
    return module;
}
