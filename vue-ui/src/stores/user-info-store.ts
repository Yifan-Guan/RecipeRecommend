import {defineStore} from 'pinia'
import {getAllUsers, addUser} from '@/hooks/user-manage'
import {type User} from '@/types'

export const useUserInfoStore = defineStore('userInfo', {
    state: () => ({
        isLoggedIn: false,
        currentUser: {id: "guest", name: "Guest"} as { id: string, name: string } | null,
        userList: [{}] as Array<User>
    }),
    getters: {
        getUserList: (state) => state.userList,
        getUser: (state) => (id: string) => {
            return state.userList.find(user => user.id == id)
        },
        getUserByName: (state) => (name: string) => {
            let user = state.userList.find(user => user.name == name)
            console.log('getUserByName:', name, user)
            return user
        }
    },
    actions: {
        async fetchAllUsers() {
            try {
                this.userList = []
                const users = await getAllUsers()
                users.map((user: [string, string, string]) => {
                    this.userList.push({
                        id: user[0],
                        name: user[1],
                        password: user[2]
                    })
                })
            } catch (error) {
                console.error("Error fetching users:", error)
            }
        },
        addUser(user: { id: string, name: string, password: string }) {
            this.userList.push(user)
        },
        userExists(name: string) {
            return this.userList.some(user => user.name === name)
        },
        setCurrentUser(user: { id: string, name: string }) {
            this.currentUser = user
            this.isLoggedIn = true
        },
        logIn(user: { name: string, password: string }) {
            const foundUser = this.getUserByName(user.name)
            if (foundUser && foundUser.password === user.password) {
                this.setCurrentUser({ id: foundUser.id, name: foundUser.name })
                return true
            }
            return false
        },
        async signUp(user: { name: string, password: string }) {
            if (!this.userExists(user.name)) {
                this.addUser({
                    id: (this.userList.length + 1).toString(),
                    name: user.name,
                    password: user.password
                })
                const response = await addUser({
                    id: (this.userList.length + 1).toString(),
                    name: user.name,
                    password: user.password
                })
                if (response.message === 'User added successfully') {
                    return true
                }
            }
            return false
        }
    }
})