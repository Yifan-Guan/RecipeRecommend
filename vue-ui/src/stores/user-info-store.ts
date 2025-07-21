import {defineStore} from 'pinia'

export const useUserInfoStore = defineStore('userInfo', {
    state: () => ({
        isLoggedIn: false,
        currentUser: null as { id: string, name: string } | null,
        userList: [{
            id: '0',
            name: 'admin',
            password: 'admin123'
        }] as Array<{
            id: string,
            name: string,
            password: string,
        }>
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
        signIn(user: { name: string, password: string }) {
            if (!this.userExists(user.name)) {
                this.addUser({
                    id: (this.userList.length + 1).toString(),
                    name: user.name,
                    password: user.password
                })
            }
        }
    }
})