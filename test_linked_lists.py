import pytest
import linked_list
import sys
import copy


ll_ref = linked_list.LinkedList()
ll_ref.append(1)
ll_ref.append(2)
ll_ref.append(3)


dll_ref = linked_list.DoubleLinkedList()
dll_ref.append(1)
dll_ref.append(2)
dll_ref.append(3)


def test_init_node():
    with pytest.raises(ValueError):
        linked_list.Node("f", 4)


def test_init_double_node():
    with pytest.raises(ValueError):
        linked_list.DoubleNode("f", 4)
    with pytest.raises(ValueError):
        linked_list.DoubleNode("f", None, 4)


def test_reference_ll():
    ll = copy.deepcopy(ll_ref)
    assert [sys.getrefcount(ll.head), sys.getrefcount(ll.head.next_node),
            sys.getrefcount(ll.head.next_node.next_node)] == [2, 2, 2]


def test_reference_dll():
    dll = copy.deepcopy(dll_ref)
    assert [sys.getrefcount(dll.head), sys.getrefcount(dll.head.next_node),
            sys.getrefcount(dll.head.next_node.next_node)] == [2, 2, 3]
    assert str(dll.head) == str(f"({dll[0]})")
    assert dll.head.prev_node is None


def test_str_node():
    assert str(linked_list.Node(3)) == "(3)"


def test_str():
    ll = copy.deepcopy(ll_ref)
    assert str(ll) == "(1)->(2)->(3)"


def test_str_dll():
    dll = copy.deepcopy(dll_ref)
    assert str(dll) == "(1)<->(2)<->(3)"


def test_getitem():
    ll = copy.deepcopy(ll_ref)
    item = "f"
    with pytest.raises(TypeError):
        print(ll[item])

    item = 999
    with pytest.raises(IndexError):
        print(ll[item])

    assert ll[0] == 1
    assert ll[1] == 2


def test_setitem():
    ll = copy.deepcopy(ll_ref)
    key = "f"
    with pytest.raises(TypeError):
        ll[key] = key

    key = 999
    with pytest.raises(IndexError):
        ll[key] = key

    ll[0] = 42
    ll[1] = 43
    assert ll[0] == 42
    assert ll[1] == 43


def test_delete_in_ll():
    ll = copy.deepcopy(ll_ref)
    with pytest.raises(ValueError):
        ll.delete(len(ll))
    ll.delete(1)
    for node in range(len(ll)):
        del(ll[0])
    assert len(ll) == 0


def test_delete_in_dll():
    dll = copy.deepcopy(dll_ref)
    dll.append(4)
    with pytest.raises(ValueError):
        dll.delete(len(dll))
    dll.delete(1)
    for node in range(len(dll)):
        del(dll[0])
    assert len(dll) == 0


def test_iter():
    ll = copy.deepcopy(ll_ref)
    ll_iter = ll.__iter__()
    i = 0
    for _ in range(len(ll)):
        assert next(ll_iter) == ll[i]
        i += 1
        
        
def test_insert_ll_bad():
    ll = copy.deepcopy(ll_ref)
    with pytest.raises(ValueError):
        ll.insert(2, -2)
    with pytest.raises(ValueError):
        ll.insert(2, len(ll) + 1)


def test_insert_dll_bad():
    dll = copy.deepcopy(dll_ref)
    with pytest.raises(ValueError):
        dll.insert(2, -2)
    with pytest.raises(ValueError):
        dll.insert(2, len(dll) + 1)


def test_insert_ll_good():
    ll = copy.deepcopy(ll_ref)
    new_item = 3
    ll.insert(new_item, 0)
    ll.insert(new_item, len(ll))
    assert ll[0] == new_item
    assert ll[len(ll)-1] == new_item


def test_insert_dll_good():
    dll = copy.deepcopy(dll_ref)
    new_item = 3
    dll.insert(new_item, 0)
    dll.insert(new_item, len(dll))
    assert dll[0] == new_item
    assert dll[len(dll)-1] == new_item


def test_clear_ll():
    ll = copy.deepcopy(ll_ref)
    ll.clear()
    assert len(ll) == 0


def test_clear_dll():
    dll = copy.deepcopy(dll_ref)
    dll.clear()
    assert len(dll) == 0


def test_index():
    ll = copy.deepcopy(ll_ref)
    assert ll.index(2) == 1
    with pytest.raises(ValueError):
        ll.index(-1)
